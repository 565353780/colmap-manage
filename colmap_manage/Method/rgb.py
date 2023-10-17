import os
import cv2
import shutil
from tqdm import tqdm

def convertImageFolderChannel(source_image_folder_path, target_image_folder_path,
                              convert_tag, print_progress=False):
    if not os.path.exists(source_image_folder_path):
        print('[ERROR][rgb::convertImageFolderChannel]')
        print('\t source image folder not exist!')
        print('\t source_image_folder_path:', source_image_folder_path)
        return False

    source_image_file_name_list = os.listdir(source_image_folder_path)

    for_data = source_image_file_name_list
    if print_progress:
        print('[ERROR][rgb::convertImageFolderChannel]')
        print('\t start convert RGB channels for images...')
        for_data = tqdm(for_data)

    if os.path.exists(target_image_folder_path):
        shutil.rmtree(target_image_folder_path)
    os.makedirs(target_image_folder_path, exist_ok=True)

    for image_file_name in for_data:
        if image_file_name.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
            continue

        source_image_file_path = source_image_folder_path + image_file_name
        target_image_file_path = target_image_folder_path + image_file_name

        source_image = cv2.imread(source_image_file_path)
        target_image = cv2.cvtColor(source_image, convert_tag)

        cv2.imwrite(target_image_file_path, target_image)
    return True
