import os
import shutil

from colmap_manage.Config.colmap import COLMAP_PATH
from colmap_manage.Method.colmap import (
    exhaustiveMatcher,
    featureExtractor,
    imageUndistorer,
    mapper,
)


class COLMAPManager(object):
    def __init__(self,
                 data_folder_path=None,
                 colmap_path=COLMAP_PATH):
        self.data_folder_path = None

        assert os.path.exists(colmap_path)
        self.colmap_path = colmap_path

        if data_folder_path is not None:
            assert self.loadData(data_folder_path)
        return


    def loadData(self, data_folder_path):
        self.data_folder_path = None

        if not os.path.exists(data_folder_path):
            print('[ERROR][COLMAPManager::loadData]')
            print('\t data_folder_path not exist!')
            print('\t data_folder_path:', data_folder_path)
            return False

        self.data_folder_path = data_folder_path
        if self.data_folder_path[-1] != '/':
            self.data_folder_path += '/'

        if not os.path.exists(self.data_folder_path + 'input/'):
            print('[ERROR][COLMAPManager::loadData]')
            print('\t input subfolder not exist!')
            print('\t input subfolder path:', self.data_folder_path + 'input/')
            self.data_folder_path = None
            return False

        return True

    def generateData(self,
                     remove_old=False,
                     database_path='distorted/database.db',
                     image_path='input/',
                     sparse_path='distorted/sparse/',
                     camera_model='PINHOLE',
                     ba_global_function_tolerance=0.000001,
                     undistort_path='',
                     output_type='COLMAP',
                     use_gpu=True):
        if self.data_folder_path is None:
            print('[ERROR][COLMAPManager::generateData]')
            print('\t data_folder_path is None!')
            return False

        if remove_old:
            dir_list = os.listdir(self.data_folder_path)
            for dir in dir_list:
                dir_path = self.data_folder_path + dir
                if os.path.isdir(dir_path):
                    if dir == 'input':
                        continue

                    shutil.rmtree(dir_path)
                else:
                    os.remove(dir_path)

        if not os.path.exists(self.data_folder_path + database_path):
            print('[INFO][COLMAPManager::generateData]')
            print('\t start featureExtractor...')
            if not featureExtractor(self.colmap_path,
                                    self.data_folder_path,
                                    database_path,
                                    image_path,
                                    camera_model,
                                    use_gpu):
                print('[ERROR][COLMAPManager::generateData]')
                print('\t featureExtractor failed!')
                return False
            print('\t featureExtractor finished!')

            print('[INFO][COLMAPManager::generateData]')
            print('\t start exhaustiveMatcher...')
            if not exhaustiveMatcher(self.colmap_path,
                                     self.data_folder_path,
                                     database_path,
                                     use_gpu):
                print('[ERROR][COLMAPManager::generateData]')
                print('\t exhaustiveMatcher failed!')
                return False
            print('\t exhaustiveMatcher finished!')

        if not os.path.exists(self.data_folder_path + sparse_path):
            print('[INFO][COLMAPManager::generateData]')
            print('\t start mapper...')
            if not mapper(self.colmap_path,
                          self.data_folder_path,
                          database_path,
                          image_path,
                          sparse_path,
                          ba_global_function_tolerance):
                print('[ERROR][COLMAPManager::generateData]')
                print('\t mapper failed!')
                return False
            print('\t mapper finished!')

        print('[INFO][COLMAPManager::generateData]')
        print('\t start imageUndistorer...')
        if not imageUndistorer(self.colmap_path,
                               self.data_folder_path,
                               image_path,
                               sparse_path,
                               undistort_path,
                               output_type):
            print('[ERROR][COLMAPManager::generateData]')
            print('\t imageUndistorer failed!')
            return False
        print('\t imageUndistorer finished!')

        return True
