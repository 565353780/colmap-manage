from colmap_manage.Config.dataset import METHOD_DICT
from colmap_manage.Method.dataset import (
    generateGSDataset,
    generateINGPDataset,
    generateNS2Dataset,
)


class DatasetManager(object):
    def __init__(self):
        return

    def generateDataset(self, method, data_folder_path, dataset_folder_path='./output/',
                        method_dict={}):
        if method not in METHOD_DICT.keys():
            print('[ERROR][DatasetManager::generateDataset]')
            print('\t method not valid!')
            return False

        if data_folder_path[-1] != '/':
            data_folder_path += '/'

        if dataset_folder_path[-1] != '/':
            dataset_folder_path += '/'

        method_name = METHOD_DICT[method]
        print('[INFO][DatasetManager::generateDataset]')
        print('\t start generate dataset for method [', method_name + ']...')
        if method == 'gs':
            return generateGSDataset(data_folder_path, dataset_folder_path, method_dict)
        if method == 'ingp':
            return generateINGPDataset(data_folder_path, dataset_folder_path,
                                       method_dict)
        if method == 'ns2':
            return generateNS2Dataset(data_folder_path, dataset_folder_path,
                                       method_dict)

        print('[ERROR][DatasetManager::generateDataset]')
        print('\t method not defined yet! please wait the code update!')
        return False

    def autoGenerateDataset(self, data_folder_path, dataset_folder_path='./output/'):
        fail_method_name_list = []

        for method, method_name in METHOD_DICT.items():
            if not self.generateDataset(method, data_folder_path, dataset_folder_path):
                fail_method_name_list.append(method_name)

        if len(fail_method_name_list) > 0:
            print('[WARN][DatasetManager::autoGenerateDataset]')
            print('\t generateDataset for some methods failed!')
            print('\t methods are:')
            for i, method_name in enumerate(fail_method_name_list):
                print('\t\t ' + str(i+1) + ': ' + method_name)
        return True
