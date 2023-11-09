from colmap_manage.Method.cmd import runCMD


def generateMVSData(
    dataset_folder_path, max_d=192, interval_scale=1.06, print_progress=False
):
    cmd = (
        "python ../colmap-manage/colmap_manage/Method/mvs_folder.py"
        + " --dense_folder "
        + dataset_folder_path
        + " --output_folder "
        + dataset_folder_path
        + "mvs/"
        + " --max_d "
        + str(max_d)
        + " --interval_scale "
        + str(interval_scale)
    )

    if not runCMD(cmd, print_progress):
        print("[ERROR][dataset::generateMVSData]")
        print("\t runCMD failed!")
        print("\t cmd:", cmd)
        return False

    return True
