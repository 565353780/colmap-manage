import os
import subprocess
import cv2
import queue
import threading
from tqdm import tqdm
from typing import Optional


def _is_hdr_video(video_file_path: str) -> bool:
    """通过 ffprobe 检测视频是否为 HDR 格式。"""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet", "-show_streams",
                "-select_streams", "v:0", video_file_path,
            ],
            capture_output=True, text=True, timeout=30,
        )
        output = result.stdout.lower()
        hdr_indicators = ["smpte2084", "arib-std-b67", "bt2020"]
        return any(ind in output for ind in hdr_indicators)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _tonemap_video(video_file_path: str, output_path: str) -> str:
    """用 ffmpeg 将 HDR 视频 tone map 为 SDR，返回输出文件路径。"""
    cmd = [
        "ffmpeg", "-y", "-i", video_file_path,
        "-vf",
        "zscale=t=linear:npl=100,format=gbrpf32le,"
        "zscale=p=bt709,tonemap=hable:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-an", output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def _save_worker(save_queue: queue.Queue, save_folder_path: str) -> None:
    """工作线程：从队列取帧并保存到磁盘。"""
    while True:
        item = save_queue.get()
        if item is None:
            save_queue.task_done()
            break
        save_idx, frame = item
        path = save_folder_path + f"{save_idx:06d}.png"
        cv2.imwrite(path, frame)
        save_queue.task_done()


def videoToImages(
    video_file_path,
    save_image_folder_path,
    down_sample_scale=1,
    target_image_num: Optional[int]=None,
    scale=1,
    show_image=False,
    print_progress=False,
    save_queue_size: int = 4,
):
    if save_image_folder_path[-1] != "/":
        save_image_folder_path += "/"

    os.makedirs(save_image_folder_path, exist_ok=True)

    tonemap_tmp_path = None
    actual_video_path = video_file_path

    if _is_hdr_video(video_file_path):
        if print_progress:
            print("[INFO][video::videoToImages]")
            print("\t HDR video detected, tone mapping to SDR ...")
        base, _ = os.path.splitext(video_file_path)
        tonemap_tmp_path = base + "_SDR.mp4"
        if not os.path.exists(tonemap_tmp_path):
            _tonemap_video(video_file_path, tonemap_tmp_path)
        elif print_progress:
            print("\t SDR file already exists, skipping tone mapping.")
        actual_video_path = tonemap_tmp_path

    cap = cv2.VideoCapture(actual_video_path)

    total_image_num = int(cap.get(7))

    if target_image_num is not None:
        if target_image_num >= total_image_num:
            down_sample_scale = 1
        else:
            down_sample_scale = int(total_image_num / target_image_num)

    for_data = range(total_image_num)

    save_idx = 1
    if print_progress:
        print("[INFO][video::videoToImages]")
        print("\t start convert video to images...")
        for_data = tqdm(for_data)

    save_queue = queue.Queue(maxsize=save_queue_size)
    saver = threading.Thread(
        target=_save_worker,
        args=(save_queue, save_image_folder_path),
        daemon=False,
    )
    saver.start()

    try:
        for image_idx in for_data:
            status, frame = cap.read()
            if not status:
                break

            image_idx += 1

            if image_idx % down_sample_scale != 0:
                continue

            if scale != 1:
                frame = cv2.resize(
                    frame,
                    (int(frame.shape[1] / scale), int(frame.shape[0] / scale)),
                )

            if show_image:
                cv2.imshow("image", frame)
                cv2.waitKey(1)

            save_queue.put((save_idx, frame.copy()))
            save_idx += 1
    finally:
        save_queue.put(None)
        save_queue.join()
        saver.join()
        if tonemap_tmp_path and os.path.exists(tonemap_tmp_path):
            os.remove(tonemap_tmp_path)

    return True
