import os
import shutil

from colmap_manage.Config.colmap import COLMAP_PATH
from colmap_manage.Method.video import videoToImages
from colmap_manage.Method.colmap import (
    exhaustiveMatcher,
    featureExtractor,
    imageUndistorer,
    mapper,
)


class COLMAPManager(object):
    def __init__(self,
                 data_folder_path=None,
                 video_file_path=None,
                 down_sample_scale=1,
                 scale=1,
                 show_image=False,
                 print_progress=False,
                 colmap_path=COLMAP_PATH):
        assert os.path.exists(colmap_path)
        self.colmap_path = colmap_path

        self.data_folder_path = None
        self.video_file_path = None
        self.down_sample_scale = 1
        self.scale = 1
        self.show_image = False
        self.print_progress = False

        if data_folder_path is not None:
            assert self.loadData(data_folder_path, video_file_path, down_sample_scale,
                                 scale, show_image, print_progress)
        return

    def reset(self):
        self.data_folder_path = None
        self.video_file_path = None
        self.down_sample_scale = 1
        self.scale = 1
        self.show_image = False
        self.print_progress = False
        return True

    def loadVideo(self):
        if self.video_file_path is None:
            return True

        assert self.video_file_path is not None
        assert self.data_folder_path is not None

        video_file_name = self.video_file_path.split('/')[-1]

        if os.path.exists(self.data_folder_path + video_file_name):
            print('[ERROR][COLMAPManager::loadVideo]')
            print('\t video is located at data_folder!' + \
                ' please set a new data_folder_path!')
            self.reset()
            return False

        if os.path.exists(self.data_folder_path):
            shutil.rmtree(self.data_folder_path)

        os.makedirs(self.data_folder_path)

        videoToImages(self.video_file_path, self.data_folder_path + 'input/',
                      self.down_sample_scale, self.scale,self.show_image,
                      self.print_progress)
        return True

    def loadData(self, data_folder_path, video_file_path=None, down_sample_scale=1,
                 scale=1, show_image=False, print_progress=False):
        self.data_folder_path = data_folder_path
        self.data_folder_path = data_folder_path
        self.video_file_path = video_file_path
        self.down_sample_scale = down_sample_scale
        self.scale = scale
        self.show_image = show_image
        self.print_progress = print_progress

        if self.data_folder_path[-1] != '/':
            self.data_folder_path += '/'

        if not self.loadVideo():
            print('[ERROR][COLMAPManager::loadData]')
            print('\t loadVideo failed!')
            print('\t video_file_path:', video_file_path)
            return False

        if not os.path.exists(data_folder_path):
            print('[ERROR][COLMAPManager::loadData]')
            print('\t data_folder_path not exist!')
            print('\t data_folder_path:', data_folder_path)
            return False

        if not os.path.exists(self.data_folder_path + 'input/'):
            print('[ERROR][COLMAPManager::loadData]')
            print('\t input subfolder not exist!')
            print('\t input subfolder path:', self.data_folder_path + 'input/')
            self.data_folder_path = None
            return False

        return True

    def removeGeneratedData(self):
        dir_list = os.listdir(self.data_folder_path)
        for dir in dir_list:
            dir_path = self.data_folder_path + dir
            if os.path.isdir(dir_path):
                if dir == 'input':
                    continue

                shutil.rmtree(dir_path)
            else:
                os.remove(dir_path)
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
            self.removeGeneratedData()

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

    def autoGenerateData(self,
                         remove_old=True,
                         valid_percentage=0.8,
                         database_path='distorted/database.db',
                         image_path='input/',
                         sparse_path='distorted/sparse/',
                         camera_model='PINHOLE',
                         ba_global_function_tolerance=0.000001,
                         undistort_path='',
                         output_type='COLMAP',
                         use_gpu=True):
        if remove_old:
            self.removeGeneratedData()

        input_image_num = len(os.listdir(self.data_folder_path + image_path))
        valid_image_num = int(valid_percentage * input_image_num)

        current_image_num = 0
        if os.path.exists(self.data_folder_path + 'images/'):
            current_image_num = len(os.listdir(self.data_folder_path + 'images/'))

        iter_idx = 0
        while current_image_num < valid_image_num:
            self.generateData(True, database_path, image_path, sparse_path,
                              camera_model, ba_global_function_tolerance,
                              undistort_path, output_type, use_gpu)

            current_image_num = len(os.listdir(self.data_folder_path + 'images/'))
            current_percentage = int((1.0 * current_image_num / \
                input_image_num) * 100)
            iter_idx += 1
            print('[INFO][COLMAPManager::autoGenerateData]')
            print('\t finish iteration: [' + str(iter_idx) + '],' + \
                ' current percentage: ' + str(current_percentage) + '%')
        return True
