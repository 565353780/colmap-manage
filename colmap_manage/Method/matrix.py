import numpy as np
from scipy.spatial.transform import Rotation as R

def getCameraMatrix(camera_info_dict):
    fx = camera_info_dict['fx']
    fy = camera_info_dict['fy']
    cx = camera_info_dict['cx']
    cy = camera_info_dict['cy']

    return np.array([
        [fx, 0.0, cx],
        [0.0, fy, cy],
        [0.0, 0.0, 1.0],
    ])

def getImageMatrix(image_pose_dict):
    r = R.from_quat(image_pose_dict['quat'])
    image_matrix = np.zeros((4, 4))
    image_matrix[:3, :3] = r.as_matrix()
    image_matrix[:3, 3] = image_pose_dict['pos']
    image_matrix[3, 3] = 1.0

    return image_matrix

def getImageInverseMatrix(image_pose_dict):
    image_matrix = getImageMatrix(image_pose_dict)

    image_rotation_transpose_matrix = image_matrix[:3, :3].transpose()

    image_inverse_matrix = np.zeros((4, 4), dtype=float)
    image_inverse_matrix[:3, :3] = image_rotation_transpose_matrix
    image_inverse_matrix[:3, 3] = -image_rotation_transpose_matrix.dot(image_matrix[:3, 3])
    image_inverse_matrix[3, 3] = 1.0

    return image_inverse_matrix

def getPointInWorld(image_matrix, point_in_image):
    image_transpose_matrix = image_matrix[:3, :3].transpose()
    print(image_transpose_matrix.shape)
    point_in_image_array = np.array(point_in_image, dtype=float).reshape(3, 1)
    print(point_in_image_array.shape)
    point_in_world = image_transpose_matrix.dot(point_in_image_array) - \
        image_transpose_matrix.dot(image_matrix[:3, 3].reshape(3, 1))

    return point_in_world

def getPointInImage(image_matrix, point_in_world):
    point_in_world_array = np.array(point_in_world, dtype=float).reshape(3, 1)
    point_in_image = image_matrix[:3, :3].dot(point_in_world_array) + \
        image_matrix[:3, 3].reshape(3, 1)

    return point_in_image
