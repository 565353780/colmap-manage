import os
import numpy as np

def loadImagePoseDictDict(images_file_path):
    if not os.path.exists(images_file_path):
        print('[ERROR][io::loadImagePoseDictDict]')
        print('\t images file not exist!')
        print('\t images_file_path:', images_file_path)
        return None

    image_pose_dict_dict = {}

    with open(images_file_path, 'r') as f:
        line_list = f.readlines()

    for line in line_list:
        if line[0] == '#':
            continue

        image_info_list = line.split(' ')
        pos = np.array([
            float(image_info_list[1]),
            float(image_info_list[2]),
            float(image_info_list[3]),
        ], dtype=float)
        quat = np.array([
            float(image_info_list[4]),
            float(image_info_list[5]),
            float(image_info_list[6]),
            float(image_info_list[7]),
        ], dtype=float)
        image_file_name = image_info_list[-1].split('\n')[0]

        image_pose_dict_dict[image_file_name] = {
            'pos': pos,
            'quat': quat,
        }

    return image_pose_dict_dict

def loadCameraInfoDict(cameras_file_path):
    if not os.path.exists(cameras_file_path):
        print('[ERROR][io::loadCameraInfoDict]')
        print('\t cameras file not exist!')
        print('\t cameras_file_path:', cameras_file_path)
        return None

    with open(cameras_file_path, 'r') as f:
        line_list = f.readlines()

    camera_info_list = []
    for line in line_list:
        if line[0] == '#':
            continue

        camera_info_list = line.split(' ')

    camera_info_dict = {
        'width': int(camera_info_list[2]),
        'height': int(camera_info_list[3]),
    }

    camera_type = camera_info_list[1]

    if camera_type[:7] == 'SIMPLE_':
        camera_info_dict.update(
            {
                'fx': float(camera_info_list[4]),
                'fy': float(camera_info_list[4]),
                'cx': float(camera_info_list[5]),
                'cy': float(camera_info_list[6]),
            }
        )
    else:
        camera_info_dict.update(
            {
                'fx': float(camera_info_list[4]),
                'fy': float(camera_info_list[5]),
                'cx': float(camera_info_list[6]),
                'cy': float(camera_info_list[7]),
            }
        )

    return camera_info_dict

def loadPointPosRgbList(points_file_path):
    if not os.path.exists(points_file_path):
        print('[ERROR][io::loadPointPosRgbList]')
        print('\t points file not exist!')
        print('\t points_file_path:', points_file_path)
        return None, None

    point_pos_list = []
    point_rgb_list = []

    with open(points_file_path, 'r') as f:
        line_list = f.readlines()

    for line in line_list:
        if line[0] == '#':
            continue

        point_info_list = line.split(' ')
        pos = [
            float(point_info_list[1]),
            float(point_info_list[2]),
            float(point_info_list[3]),
        ]
        rgb = [
            float(point_info_list[4]) / 255.0,
            float(point_info_list[5]) / 255.0,
            float(point_info_list[6]) / 255.0,
        ]

        point_pos_list.append(pos)
        point_rgb_list.append(rgb)

    point_pos_list = np.array(point_pos_list, dtype=float)
    point_rgb_list = np.array(point_rgb_list, dtype=float)
    return point_pos_list, point_rgb_list

def loadPointPosRgbArray(points_file_path):
    point_pos_list, point_rgb_list = loadPointPosRgbList(points_file_path)

    if point_pos_list is None:
        print('[ERROR][io::loadPointPosRgbArray]')
        print('\t loadPointPosRgbList failed!')
        return None, None

    point_pos_array = np.array(point_pos_list, dtype=float)
    point_rgb_array = np.array(point_rgb_list, dtype=float)
    return point_pos_array, point_rgb_array
