import os
from pathlib import Path
import shutil

def print_task_parameters(task):
        print("  → {:<30} {:<30}".format('Parameter','Value'))
        for param, value in task['parameters'].items():
            print("  → {:<30} {:<30}".format(param, value))

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def rm_folder_content(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))