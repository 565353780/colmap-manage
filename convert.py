from colmap_manage.Module.colmap_manager import COLMAPManager
from colmap_manage.Module.dataset_manager import DatasetManager

data_folder_path = "/home/chli/Dataset/NeRF/hotdog_train/"
video_file_path = "/home/chli/chLi/Dataset/NeRF/3vjia_person_2/1.mp41"
video_file_path = None
down_sample_scale = 1

scale = 1
show_image = False
print_progress = True
remove_old = False
remain_db = True
valid_percentage = 0.8
run_mvs = False
dataset_folder_path = "../colmap-manage/output/3vjia_simple/"
method_name = "gs"
method_dict = {}
is_copy = False

COLMAPManager(data_folder_path, video_file_path).autoGenerateData(
    remove_old, remain_db, valid_percentage, run_mvs=run_mvs
)
# DatasetManager().generateDataset(
#    "gs", data_folder_path, dataset_folder_path, method_dict, is_copy, print_progress
# )
DatasetManager().autoGenerateDataset(
    data_folder_path, dataset_folder_path, is_copy, print_progress
)
