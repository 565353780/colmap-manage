import numpy as np
from wis3d import Wis3D
from colmap_manage.Method.matrix import (
    getCameraMatrix,
    getImageMatrix,
    getImageInverseMatrix,
    getPointInWorld,
    getPointInImage,
)

def renderImagePose(image_pose_dict_dict, camera_info_dict, point_pos_array, point_rgb_array):
    wis3d = Wis3D("./output/test1/", 'test1', xyz_pattern=('x', 'y', 'z'))
    wis3d.add_point_cloud(point_pos_array, point_rgb_array, name='pointcloud')

    camera_matrix = getCameraMatrix(camera_info_dict)

    for i, image_pose_dict in enumerate(image_pose_dict_dict.values()):
        image_inverse_matrix = getImageInverseMatrix(image_pose_dict)

        wis3d.add_camera_pose(image_inverse_matrix, name="camera_pose_" + str(i))
    return True
