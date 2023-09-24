from colmap_manage.Module.colmap_manager import COLMAPManager


def demo():
    data_folder_path = '/home/chli/chLi/Dataset/NeRF/3vjia_simple/'
    remove_old = True

    colmap_manager = COLMAPManager(data_folder_path)
    colmap_manager.generateData(remove_old)
    return True
