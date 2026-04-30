import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Render COLMAP reconstruction.")
parser.add_argument(
    "folder_path",
    type=str,
    help="Path to the COLMAP output folder (e.g. .../01_colmap/).",
)
parser.add_argument(
    "--cuda",
    type=int,
    default=0,
    metavar="N",
    help="CUDA device id for CUDA_VISIBLE_DEVICES (default: 0).",
)
args = parser.parse_args()

os.environ["CUDA_VISIBLE_DEVICES"] = str(args.cuda)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

from colmap_manage.Module.colmap_renderer import COLMAPRenderer

COLMAPRenderer.renderColmap(args.folder_path)
