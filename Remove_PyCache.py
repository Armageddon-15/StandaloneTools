import os
import shutil


dest_dir = r".\dist\ChannelRecompositer"


def deleteCache(d):
    d = os.path.abspath(d)
    for dirs in os.listdir(d):
        dirs = os.path.join(d, dirs)
        if os.path.isdir(dirs):
            deleteCache(dirs)
            if os.path.relpath(dirs, d) == "__pycache__":
                print("remove path", dirs)
                shutil.rmtree(dirs)


deleteCache(dest_dir)