import os
import cv2

from colmap_manage.Config.dataset import METHOD_DICT
from colmap_manage.Method.rgb import convertImageFolderChannel
from colmap_manage.Method.dataset import (
    generateGSDataset,
    generateINGPDataset,
    generateNS2Dataset,
    generateNADataset,
)


class DatasetManager(object):
    def __init__(self):
        return

    def generateRGBImage(self, data_folder_path, print_progress=False):
        images_folder_path = data_folder_path + 'images/'

        image_file_name_list = os.listdir(images_folder_path)

        test_image_file_path = images_folder_path + image_file_name_list[0]

        test_image = cv2.imread(test_image_file_path)

        channel_num = test_image.shape[2]

        if channel_num == 3:
            return True

        if channel_num != 1:
            print('[ERROR][DatasetManager::generateRGBImage]')
            print('\t channel num not vaild!')
            print('\t channel_num:', channel_num)
            return False

        gray_image_folder_path = data_folder_path + 'images_gray/'
        rgb_image_folder_path = data_folder_path + 'images/'

        os.rename(rgb_image_folder_path, gray_image_folder_path)

        if not convertImageFolderChannel(gray_image_folder_path, rgb_image_folder_path,
                                         cv2.COLOR_GRAY2BGR, print_progress):
            print('[ERROR][DatasetManager::generateRGBImage]')
            print('\t convertImageFolderChannel failed!')
            return False

        return True

    def generateDataset(self, method, data_folder_path, dataset_folder_path='./output/',
                        method_dict={}, print_progress=False):
        if method not in METHOD_DICT.keys():
            print('[ERROR][DatasetManager::generateDataset]')
            print('\t method not valid!')
            return False

        if data_folder_path[-1] != '/':
            data_folder_path += '/'

        if dataset_folder_path[-1] != '/':
            dataset_folder_path += '/'

        if not self.generateRGBImage(data_folder_path, print_progress):
            print('[ERROR][DatasetManager::generateDataset]')
            print('\t generateRGBImage failed!')
            print('\t data_folder_path:', data_folder_path)
            return False

        method_name = METHOD_DICT[method]
        print('[INFO][DatasetManager::generateDataset]')
        print('\t start generate dataset for method [', method_name + ']...')
        if method == 'gs':
            return generateGSDataset(data_folder_path, dataset_folder_path,
                                       method_dict, print_progress)
        if method == 'ingp':
            return generateINGPDataset(data_folder_path, dataset_folder_path,
                                       method_dict, print_progress)
        if method == 'ns2':
            return generateNS2Dataset(data_folder_path, dataset_folder_path,
                                       method_dict, print_progress)
        if method == 'na':
            return generateNADataset(data_folder_path, dataset_folder_path,
                                       method_dict, print_progress)

        print('[ERROR][DatasetManager::generateDataset]')
        print('\t method not defined yet! please wait the code update!')
        return False

    def autoGenerateDataset(self, data_folder_path, dataset_folder_path='./output/',
                                print_progress=False):
        fail_method_name_list = []

        for method, method_name in METHOD_DICT.items():
            if not self.generateDataset(method, data_folder_path, dataset_folder_path,
                                            {}, print_progress):
                fail_method_name_list.append(method_name)

        if len(fail_method_name_list) > 0:
            print('[WARN][DatasetManager::autoGenerateDataset]')
            print('\t generateDataset for some methods failed!')
            print('\t methods are:')
            for i, method_name in enumerate(fail_method_name_list):
                print('\t\t ' + str(i+1) + ': ' + method_name)
        return True
