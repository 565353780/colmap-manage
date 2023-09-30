import os

def loadImagePoseDict(images_file_path):
    if not os.path.exists(images_file_path):
        print('[ERROR][io::loadImagePoseDict]')
        print('\t images file not exist!')
        print('\t images_file_path:', images_file_path)
        return None

    image_pose_dict = {}

    with open(images_file_path, 'r') as f:
        line_list = f.readlines()

    for line in line_list:
        if line[0] == '#':
            continue

        image_info_list = line.split(' ')
        position = [
            float(image_info_list[1]),
            float(image_info_list[2]),
            float(image_info_list[3]),
        ]
        quat = [
            float(image_info_list[4]),
            float(image_info_list[5]),
            float(image_info_list[6]),
            float(image_info_list[7]),
        ]
        image_file_name = image_info_list[-1].split('\n')[0]

        image_pose_dict[image_file_name] = {
            'position': position,
            'quat': quat,
        }

    return image_pose_dict

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