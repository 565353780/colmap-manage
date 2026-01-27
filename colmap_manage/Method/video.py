import os
import cv2
from tqdm import tqdm
from typing import Optional


def videoToImages(
    video_file_path,
    save_image_folder_path,
    down_sample_scale=1,
    target_image_num: Optional[int]=None,
    scale=1,
    show_image=False,
    print_progress=False,
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
    for image_idx in for_data:
        status, frame = cap.read()
        if not status:
            break

        image_idx += 1

        if image_idx % down_sample_scale != 0:
            continue

        if scale != 1:
            frame = cv2.resize(
                frame, (int(frame.shape[1] / scale), int(frame.shape[0] / scale))
            )

        if show_image:
            cv2.imshow("image", frame)
            cv2.waitKey(1)

        save_image_file_path = (
            save_image_folder_path + f"{save_idx:06d}.png"
        )
        cv2.imwrite(save_image_file_path, frame)

        save_idx += 1
    return True
