import os
from colmap_manage.Method.io import (
    loadImagePoseDictDict,
    loadCameraInfoDict,
    loadPointPosRgbArray,
)
from colmap_manage.Method.render import renderImagePose

class ImagePoseRenderer(object):
    def __init__(self) -> None:
        return

    def renderImages(self, data_folder_path):
        images_file_path = data_folder_path + 'sparse/images.txt'
        cameras_file_path = data_folder_path + 'sparse/cameras.txt'
        points_file_path = data_folder_path + 'sparse/points3D.txt'

        image_pose_dict_dict = loadImagePoseDictDict(images_file_path)
        camera_info_dict = loadCameraInfoDict(cameras_file_path)
        point_pos_array, point_rgb_array = loadPointPosRgbArray(points_file_path)

        renderImagePose(image_pose_dict_dict, camera_info_dict, point_pos_array, point_rgb_array)
        return True
