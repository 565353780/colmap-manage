import os
import cv2
import queue
import threading
from tqdm import tqdm
from typing import Optional


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

    cap = cv2.VideoCapture(video_file_path)

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

    return True
