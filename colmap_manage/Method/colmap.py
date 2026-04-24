import os
import shutil
from colmap_manage.Method.cmd import runCMD
from colmap_manage.Method.path import createFileFolder


def getColmapGPUIndex():
    '''
    根据 CUDA_VISIBLE_DEVICES 环境变量返回 colmap 可使用的 gpu_index 字符串。

    Returns:
        - None: 环境变量未设置，colmap 按默认逻辑使用全部可见 GPU
        - '-1': 环境变量为空字符串，表示不使用 GPU
        - '0' / '0,1,...': 环境变量重映射后的 GPU 索引列表
    '''
    if 'CUDA_VISIBLE_DEVICES' not in os.environ:
        return None

    cuda_visible = os.environ['CUDA_VISIBLE_DEVICES'].strip()
    if cuda_visible == '':
        return '-1'

    gpu_list = [g.strip() for g in cuda_visible.split(',') if g.strip() != '']
    if len(gpu_list) == 0:
        return '-1'

    # CUDA_VISIBLE_DEVICES 会对子进程重映射 GPU 索引，从 0 开始连续编号
    return ','.join(str(i) for i in range(len(gpu_list)))


def featureExtractor(
    colmap_path: str,
    data_folder_path: str,
    database_path: str='database.db',
    image_path: str='input/',
    camera_model: str='PINHOLE',
    use_gpu: bool=False,
    print_progress: bool=False,
) -> bool:
    '''
    Inputs:
        input/<images>
    Outputs:
        database.db
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    createFileFolder(data_folder_path + database_path)

    gpu_index = getColmapGPUIndex()
    if gpu_index == '-1':
        use_gpu = False
    gpu_tag = '1' if use_gpu else '0'

    cmd = colmap_path + ' feature_extractor' + \
        ' --database_path ' + data_folder_path + database_path + \
        ' --image_path ' + data_folder_path + image_path + \
        ' --ImageReader.single_camera ' + '1' + \
        ' --ImageReader.camera_model ' + camera_model + \
        ' --FeatureExtraction.use_gpu ' + gpu_tag

    if use_gpu and gpu_index is not None:
        cmd += ' --FeatureExtraction.gpu_index ' + gpu_index

    result = runCMD(cmd, print_progress)
    if result is None:
        print('[ERROR][colmap::featureExtractor]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def exhaustiveMatcher(
    colmap_path: str,
    data_folder_path: str,
    database_path: str='database.db',
    use_gpu: bool=False,
    print_progress: bool=False
) -> bool:
    '''
    Inputs:
        database.db
    Outputs:
        database.db
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    gpu_index = getColmapGPUIndex()
    if gpu_index == '-1':
        use_gpu = False
    gpu_tag = '1' if use_gpu else '0'

    cmd = colmap_path + ' exhaustive_matcher' + \
        ' --database_path ' + data_folder_path + database_path + \
        ' --FeatureMatching.use_gpu ' + gpu_tag

    if use_gpu and gpu_index is not None:
        cmd += ' --FeatureMatching.gpu_index ' + gpu_index

    result = runCMD(cmd, print_progress)
    if result is None:
        print('[ERROR][colmap::exhaustiveMatcher]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def mapper(colmap_path,
           data_folder_path,
           database_path='database.db',
           image_path='input/',
           sparse_path='sparse/',
           print_progress=False):
    '''
    Inputs:
        input/<images>
        database.db
    Outputs:
        sparse/0/cameras.bin #Camera internal params
        sparse/0/images.bin #Camera poses
        sparse/0/points3D.bin #Sparse 3D points
        sparse/0/project.ini
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    os.makedirs(data_folder_path + sparse_path, exist_ok=True)

    cmd = colmap_path + ' mapper' + \
        ' --database_path ' + data_folder_path + database_path + \
        ' --image_path ' + data_folder_path + image_path + \
        ' --output_path ' + data_folder_path + sparse_path

    result = runCMD(cmd, print_progress)
    if result is None:
        print('[ERROR][colmap::mapper]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def imageUndistorer(colmap_path,
                    data_folder_path,
                    image_path='input/',
                    sparse_path='sparse/',
                    dense_path='dense/',
                    output_type='COLMAP',
                    print_progress=False):
    '''
    Inputs:
        input/<images>
        sparse/0/cameras.bin #Camera internal params
        sparse/0/images.bin #Camera poses
        sparse/0/points3D.bin #Sparse 3D points
        sparse/0/project.ini
    Outputs:
        dense/images/<images>
        dense/sparse/cameras.bin #Camera internal params
        dense/sparse/images.bin #Camera poses
        dense/sparse/points3D.bin #Sparse 3D points
        dense/stereo/<with configs only>...
        dense/run-*.sh
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    cmd = colmap_path + ' image_undistorter' + \
        ' --image_path ' + data_folder_path + image_path + \
        ' --input_path ' + data_folder_path + sparse_path + '0/' + \
        ' --output_path ' + data_folder_path + dense_path + \
        ' --output_type ' + output_type

    result = runCMD(cmd, print_progress)
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

def patchMatchStereo(
    colmap_path: str,
    data_folder_path: str,
    dense_path: str = 'dense/',
    print_progress: bool = False) -> bool:
    '''
    Inputs:
        dense/images/<images>
        dense/sparse/cameras.bin #Camera internal params
        dense/sparse/images.bin #Camera poses
        dense/sparse/points3D.bin #Sparse 3D points
        dense/stereo/<with configs only>...
        dense/run-*.sh
    Outputs:
        dense/stereo/depth_maps/<data>...
        dense/stereo/depth_maps/fusion.cfg...
        dense/stereo/normal_maps/<data>...
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    gpu_index = getColmapGPUIndex()

    cmd = colmap_path + ' patch_match_stereo' + \
        ' --workspace_path ' + data_folder_path + dense_path + \
        ' --workspace_format ' + 'COLMAP' + \
        ' --PatchMatchStereo.geom_consistency ' + 'true'

    if gpu_index is not None:
        cmd += ' --PatchMatchStereo.gpu_index ' + gpu_index

    result = runCMD(cmd, print_progress)
    if result is None:
        print('[ERROR][colmap::patchMatchStereo]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def stereoFusion(
    colmap_path: str,
    data_folder_path: str,
    dense_path: str = 'dense/',
    print_progress: bool = False) -> bool:
    '''
    Inputs:
        dense/stereo/depth_maps/<data>...
        dense/stereo/depth_maps/fusion.cfg...
        dense/stereo/normal_maps/<data>...
        dense/images/<images>
    Outputs:
        dense/stereo/result.ply
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    cmd = colmap_path + ' stereo_fusion' + \
        ' --workspace_path ' + data_folder_path + dense_path + \
        ' --workspace_format ' + 'COLMAP' + \
        ' --input_type ' + 'geometric' + \
        ' --output_path ' + data_folder_path + dense_path + 'result.ply'

    result = runCMD(cmd, print_progress)
    if result is None:
        print('[ERROR][colmap::stereoFusion]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def modelConverter(colmap_path,
                   data_folder_path,
                   bin_path='sparse/0/',
                   output_type='TXT',
                   print_progress=False):
    '''
    Inputs:
        <bin_path>/*.bin
    Outputs:
        <bin_path>/*.txt
    '''
    if data_folder_path[-1] != '/':
        data_folder_path += '/'

    cmd = colmap_path + ' model_converter' + \
        ' --input_path ' + data_folder_path + bin_path + \
        ' --output_path ' + data_folder_path + bin_path + \
        ' --output_type ' + output_type

    result = runCMD(cmd, print_progress)
    if result is None:
        print('[ERROR][colmap::modelConverter]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True
