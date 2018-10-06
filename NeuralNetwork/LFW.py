import shutil
import os
FOLDERS_PATH = '/home/edoardo/Downloads/lfw-deepfunneled_p'
folders = os.listdir(FOLDERS_PATH)
for f in folders:
    path = FOLDERS_PATH + '/' + f
    if len(os.listdir(path)) < 2:
        shutil.rmtree(path)