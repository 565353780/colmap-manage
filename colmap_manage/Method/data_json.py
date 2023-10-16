from colmap_manage.Method.cmd import runCMD

def generateINGPJsonData(dataset_folder_path, aabb_scale=8, print_progress=False):
    cmd = 'python ../colmap-manage/colmap_manage/Method/ingp_json.py' + \
        ' --images ' + dataset_folder_path + 'images/' + \
        ' --text ' + dataset_folder_path + 'sparse/0/' + \
        ' --out ' + dataset_folder_path + 'transform.json' + \
        ' --aabb_scale ' + str(aabb_scale) + \
        ' --abs_path'

    if not runCMD(cmd, print_progress):
        print('[ERROR][dataset::generateINGPJsonData]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def generateNS2JsonData(dataset_folder_path, aabb_scale=8, print_progress=False):
    cmd = 'python ../colmap-manage/colmap_manage/Method/ingp_json.py' + \
        ' --images ' + dataset_folder_path + 'images/' + \
        ' --text ' + dataset_folder_path + 'sparse/0/' + \
        ' --out ' + dataset_folder_path + 'transform.json' + \
        ' --aabb_scale ' + str(aabb_scale)

    if not runCMD(cmd, print_progress):
        print('[ERROR][dataset::generateNS2JsonData]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True

def generateNAJsonData(dataset_folder_path, scene_type='outdoor', print_progress=False):
    cmd = 'python ../colmap-manage/colmap_manage/Method/na_json.py' + \
        ' --data_dir ' + dataset_folder_path + \
        ' --scene_type ' + scene_type

    if not runCMD(cmd, print_progress):
        print('[ERROR][dataset::generateNAJsonData]')
        print('\t runCMD failed!')
        print('\t cmd:', cmd)
        return False

    return True
