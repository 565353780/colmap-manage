from colmap_manage.Config.dataset import METHOD_DICT
from colmap_manage.Method.dataset import (
    generateGSDataset,
    generateINGPDataset,
)


class DatasetManager(object):
    def __init__(self):
        return

    def generateDataset(self, method, data_folder_path, dataset_folder_path=None):
        if method not in METHOD_DICT.keys():
            print('[ERROR][DatasetManager::generateDataset]')
            print('\t method not valid!')
            return False

        if dataset_folder_path is None:
            dataset_folder_path = method + '/'

        method_name = METHOD_DICT[method]
        print('[INFO][DatasetManager::generateDataset]')
        print('\t start generate dataset for method [', method_name + ']...')
        if method == 'gs':
            return generateGSDataset(data_folder_path, dataset_folder_path)
        if method == 'ingp':
            return generateINGPDataset(data_folder_path, dataset_folder_path)

        print('[ERROR][DatasetManager::generateDataset]')
        print('\t method not defined yet! please wait the code update!')
        return False
