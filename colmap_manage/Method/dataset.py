import os
import shutil
from colmap_manage.Config.colmap import PRINT_PROGRESS
from colmap_manage.Method.cmd import runCMD

def generateDatasetByDict(data_folder_path, dataset_folder_path, method, ln_dict):
    method_dataset_folder_path = dataset_folder_path + method + '/'

    if os.path.exists(method_dataset_folder_path):
        shutil.rmtree(method_dataset_folder_path)
    os.makedirs(method_dataset_folder_path, exist_ok=True)

    for source, target in ln_dict.items():
        os.symlink(data_folder_path + source, method_dataset_folder_path + target)
    return True

def generateGSDataset(data_folder_path, dataset_folder_path='./output/',
                      method_dict={}):
    ln_dict = {
        'images/': 'images',
        'sparse/': 'sparse',
    }

    if not generateDatasetByDict(data_folder_path, dataset_folder_path, 'gs', ln_dict):
        print('[ERROR][dataset::generateGSDataset]')
        print('\t generateDatasetByDict failed!')
        print('\t dataset:', data_folder_path)
        return False

    return True

def generateTransformData(dataset_folder_path, aabb_scale=8):
    cmd = 'python ../colmap-manage/colmap_manage/Method/colmap2nerf.py' + \
        ' --images ' + dataset_folder_path + 'images/' + \
        ' --text ' + dataset_folder_path + 'sparse/0/' + \
        ' --out ' + dataset_folder_path + 'transform.json' + \
        ' --aabb_scale ' + str(aabb_scale)

    if not runCMD(cmd, PRINT_PROGRESS):
        print('[ERROR][dataset::generateTransformData]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def generateINGPDataset(data_folder_path, dataset_folder_path='./output/',
                        method_dict={}):
    ln_dict = {
        'images/': 'images',
        'sparse/': 'sparse',
    }

    aabb_scale = 8
    if 'aabb_scale' in method_dict.keys():
        aabb_scale = int(method_dict['aabb_scale'])

    if not generateDatasetByDict(data_folder_path, dataset_folder_path, 'ingp',
                                 ln_dict):
        print('[ERROR][dataset::generateINGPDataset]')
        print('\t generateDatasetByDict failed!')
        print('\t dataset:', data_folder_path)
        return False

    if not generateTransformData(dataset_folder_path + 'ingp/', aabb_scale):
        print('[ERROR][dataset::generateINGPDataset]')
        print('\t generateTransformData failed!')
        print('\t dataset:', data_folder_path)
        return False

    return True
