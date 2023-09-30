from colmap_manage.Module.image_pose_renderer import ImagePoseRenderer

def demo():
    data_folder_path = '/home/chli/chLi/Dataset/NeRF/test1/'

    image_pose_renderer = ImagePoseRenderer()
    image_pose_renderer.renderImages(data_folder_path)
    return True
