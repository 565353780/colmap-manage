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


def _tonemap_video(video_file_path: str, output_path: str) -> None:
    """用 ffmpeg 将 HDR 视频 tone map 为 SDR。

    优先使用 zscale+tonemap（需要 libzimg），
    若不可用则 fallback 到 colorspace 滤镜（ffmpeg 内置）。
    """
    pipelines = [
        (
            "zscale=t=linear:npl=100,format=gbrpf32le,"
            "zscale=p=bt709,tonemap=hable:desat=0,"
            "zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
        ),
        (
            "colorspace=bt709:iall=bt2020:fast=1,format=yuv420p"
        ),
    ]

    for i, vf in enumerate(pipelines):
        cmd = [
            "ffmpeg", "-y", "-i", video_file_path,
            "-vf", vf,
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-an", output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[INFO][video::_tonemap_video]")
            print(f"\t tone mapping succeeded with pipeline {i + 1}: {vf}")
            return

    raise RuntimeError(
        f"[ERROR][video::_tonemap_video]\n"
        f"\t all tonemap pipelines failed for: {video_file_path}\n"
        f"\t last ffmpeg stderr:\n{result.stderr}"
    )


def _save_worker(save_queue: queue.Queue, save_folder_path: str) -> None:
    """工作线程：从队列取帧并保存到磁盘。"""
    while True:
        item = save_queue.get()
        if item is None:
            save_queue.task_done()
            break
        save_idx, frame = item
        path = save_folder_path + f"{save_idx:06d}.jpg"
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

    if target_image_num is not None and target_image_num < total_image_num:
        # 始终包含第一帧(索引0)，然后均匀间隔抽取，共 target_image_num 帧
        if target_image_num <= 1:
            selected_indices = {0}
        else:
            selected_indices = set(
                round(i * (total_image_num - 1) / (target_image_num - 1))
                for i in range(target_image_num)
            )
    else:
        selected_indices = None

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

            if selected_indices is not None:
                if image_idx not in selected_indices:
                    continue
            elif (image_idx + 1) % down_sample_scale != 0:
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
