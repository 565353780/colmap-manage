import shutil

COLMAP_PATH = shutil.which('colmap')

if COLMAP_PATH is None:
    print('ERROR][Config.colmap]')
    print('\t colmap not found!')
    exit()

print("Using COLMAP at:", COLMAP_PATH)
