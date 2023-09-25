import os
import shutil

def generateDatasetByDict(data_folder_path, dataset_folder_path, method, ln_dict):
    method_dataset_folder_path = dataset_folder_path + method + '/'

    if os.path.exists(method_dataset_folder_path):
        shutil.rmtree(method_dataset_folder_path)
    os.makedirs(method_dataset_folder_path, exist_ok=True)

    for source, target in ln_dict.items():
        os.symlink(data_folder_path + source, method_dataset_folder_path + target)
    return True

def generateGSDataset(data_folder_path, dataset_folder_path='./output/'):
    ln_dict = {
        'images/': 'images',
        'sparse/': 'sparse',
    }
    return generateDatasetByDict(data_folder_path, dataset_folder_path, 'gs', ln_dict)

def generateINGPDataset(data_folder_path, dataset_folder_path='./output/'):
    ln_dict = {
        'images/': 'images',
        'sparse/': 'sparse',
    }
    return generateDatasetByDict(data_folder_path, dataset_folder_path, 'ingp', ln_dict)
