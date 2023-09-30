import os
from colmap_manage.Method.io import loadImagePoseDict, loadCameraInfoDict
from colmap_manage.Method.transform import getImagePose

class ImagePoseRenderer(object):
    def __init__(self) -> None:
        return

    def renderImages(self, data_folder_path):
        images_file_path = data_folder_path + 'sparse/images.txt'
        cameras_file_path = data_folder_path + 'sparse/cameras.txt'
        image_folder_path = data_folder_path + 'input/'

        image_pose_dict = loadImagePoseDict(images_file_path)
        camera_info_dict = loadCameraInfoDict(cameras_file_path)

        print(len(image_pose_dict.keys()))
        print(camera_info_dict)
        return True
