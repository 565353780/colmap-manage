import os
import shutil

from colmap_manage.Method.data_json import (
    generateINGPJsonData,
    generateNS2JsonData,
    generateNAJsonData,
    generateJNJsonData,
)


def generateDatasetByDict(data_folder_path, dataset_folder_path, method, ln_dict):
    method_dataset_folder_path = dataset_folder_path + method + "/"

    if os.path.exists(method_dataset_folder_path):
        shutil.rmtree(method_dataset_folder_path)
    os.makedirs(method_dataset_folder_path, exist_ok=True)

    for source, target in ln_dict.items():
        os.symlink(data_folder_path + source, method_dataset_folder_path + target)
    return True


def generateGSDataset(
    data_folder_path,
    dataset_folder_path="./output/",
    method_dict={},
    print_progress=False,
):
    ln_dict = {
        "images/": "images",
        "sparse/": "sparse",
    }

    if not generateDatasetByDict(data_folder_path, dataset_folder_path, "gs", ln_dict):
        print("[ERROR][dataset::generateGSDataset]")
        print("\t generateDatasetByDict failed!")
        print("\t dataset:", data_folder_path)
        return False

    return True


def generateINGPDataset(
    data_folder_path,
    dataset_folder_path="./output/",
    method_dict={},
    print_progress=False,
):
    ln_dict = {
        "images/": "images",
        "sparse/": "sparse",
    }

    aabb_scale = 8
    if "aabb_scale" in method_dict.keys():
        aabb_scale = int(method_dict["aabb_scale"])

    if not generateDatasetByDict(
        data_folder_path, dataset_folder_path, "ingp", ln_dict
    ):
        print("[ERROR][dataset::generateINGPDataset]")
        print("\t generateDatasetByDict failed!")
        print("\t dataset:", data_folder_path)
        return False

    if not generateINGPJsonData(
        dataset_folder_path + "ingp/", aabb_scale, print_progress
    ):
        print("[ERROR][dataset::generateINGPDataset]")
        print("\t generateINGPJsonData failed!")
        print("\t dataset:", data_folder_path)
        return False

    return True


def generateNS2Dataset(
    data_folder_path,
    dataset_folder_path="./output/",
    method_dict={},
    print_progress=False,
):
    ln_dict = {
        "images/": "images",
        "sparse/": "sparse",
    }

    aabb_scale = 8
    if "aabb_scale" in method_dict.keys():
        aabb_scale = int(method_dict["aabb_scale"])

    if not generateDatasetByDict(data_folder_path, dataset_folder_path, "ns2", ln_dict):
        print("[ERROR][dataset::generateNS2Dataset]")
        print("\t generateDatasetByDict failed!")
        print("\t dataset:", data_folder_path)
        return False

    if not generateNS2JsonData(
        dataset_folder_path + "ns2/", aabb_scale, print_progress
    ):
        print("[ERROR][dataset::generateNS2Dataset]")
        print("\t generateNS2JsonData failed!")
        print("\t dataset:", data_folder_path)
        return False

    return True


def generateNADataset(
    data_folder_path,
    dataset_folder_path="./output/",
    method_dict={},
    print_progress=False,
):
    ln_dict = {
        "images/": "images",
        "sparse/0/": "sparse",
    }

    scene_type = "outdoor"
    if "scene_type" in method_dict.keys():
        scene_type = method_dict["scene_type"]
        if scene_type not in ["outdoor", "indoor", "object"]:
            print("[ERROR][dataset::generateNADataset]")
            print("\t scene_type not valid!")
            print("\t scene_type:", scene_type)
            return False

    if not generateDatasetByDict(data_folder_path, dataset_folder_path, "na", ln_dict):
        print("[ERROR][dataset::generateNADataset]")
        print("\t generateDatasetByDict failed!")
        print("\t dataset:", data_folder_path)
        return False

    if not generateNAJsonData(dataset_folder_path + "na/", scene_type, print_progress):
        print("[ERROR][dataset::generateNADataset]")
        print("\t generateNAJsonData failed!")
        print("\t dataset:", data_folder_path)
        return False

    return True


def generateJNDataset(
    data_folder_path,
    dataset_folder_path="./output/",
    method_dict={},
    print_progress=False,
):
    ln_dict = {
        "images/": "images",
        "sparse/": "sparse",
    }

    aabb_scale = 8
    if "aabb_scale" in method_dict.keys():
        aabb_scale = int(method_dict["aabb_scale"])

    if not generateDatasetByDict(data_folder_path, dataset_folder_path, "jn", ln_dict):
        print("[ERROR][dataset::generateJNDataset]")
        print("\t generateDatasetByDict failed!")
        print("\t dataset:", data_folder_path)
        return False

    if not generateJNJsonData(dataset_folder_path + "jn/", aabb_scale, print_progress):
        print("[ERROR][dataset::generateJNDataset]")
        print("\t generateINGPJsonData failed!")
        print("\t dataset:", data_folder_path)
        return False

    return True
