import os
import shutil
from colmap_manage.Method.cmd import runCMD
from colmap_manage.Method.path import createFileFolder

def featureExtractor(colmap_path,
                     data_folder_path,
                     database_path='distorted/database.db',
                     image_path='input/',
                     camera_model='PINHOLE',
                     use_gpu=True):
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    createFileFolder(data_folder_path + database_path)

    gpu_tag = '1' if use_gpu else '0'

    cmd = colmap_path + ' feature_extractor' + \
        ' --database_path ' + data_folder_path + database_path + \
        ' --image_path ' + data_folder_path + image_path + \
        ' --ImageReader.single_camera ' + '1' + \
        ' --ImageReader.camera_model ' + camera_model + \
        ' --SiftExtraction.use_gpu ' + gpu_tag

    result = runCMD(cmd)
    if result is None:
        print('[ERROR][colmap::featureExtractor]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def exhaustiveMatcher(colmap_path,
                      data_folder_path,
                      database_path='distorted/database.db',
                      use_gpu=True):
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    gpu_tag = '1' if use_gpu else '0'

    cmd = colmap_path + ' exhaustive_matcher' + \
        ' --database_path ' + data_folder_path + database_path + \
        ' --SiftMatching.use_gpu ' + gpu_tag

    result = runCMD(cmd)
    if result is None:
        print('[ERROR][colmap::exhaustiveMatcher]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def mapper(colmap_path,
           data_folder_path,
           database_path='distorted/database.db',
           image_path='input/',
           sparse_path='distorted/sparse/',
           ba_global_function_tolerance=0.000001):
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    os.makedirs(data_folder_path + sparse_path, exist_ok=True)

    cmd = colmap_path + ' mapper' + \
        ' --database_path ' + data_folder_path + database_path + \
        ' --image_path ' + data_folder_path + image_path + \
        ' --output_path ' + data_folder_path + sparse_path + \
        ' --Mapper.ba_global_function_tolerance=' + str(ba_global_function_tolerance)

    result = runCMD(cmd)
    if result is None:
        print('[ERROR][colmap::mapper]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def imageUndistorer(colmap_path,
                    data_folder_path,
                    image_path='input/',
                    sparse_path='distorted/sparse/',
                    undistort_path='',
                    output_type='COLMAP'):
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    cmd = colmap_path + ' image_undistorter' + \
        ' --image_path ' + data_folder_path + image_path + \
        ' --input_path ' + data_folder_path + sparse_path + '0/' + \
        ' --output_path ' + data_folder_path + undistort_path + \
        ' --output_type ' + output_type

    result = runCMD(cmd)
    if result is None:
        print('[ERROR][colmap::imageUndistorer]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    os.makedirs(data_folder_path + 'sparse/0/', exist_ok=True)

    file_name_list = os.listdir(data_folder_path + 'sparse/')
    for file_name in file_name_list:
        file_path = data_folder_path + 'sparse/' + file_name
        if os.path.isdir(file_path) and file_name == '0':
            continue

        target_file_path = data_folder_path + 'sparse/0/' + file_name
        shutil.move(file_path, target_file_path)
    return True
