import shutil
import subprocess
import os
import configparser
from time import time

config_section = 'STORAGE'
params = configparser.ConfigParser()
params.read('parameters.ini')

image_path = params.get(config_section, 'path')
delete_delay = params.getint(config_section, 'delay_storage')


def get_disk_space():
    total, used, free = shutil.disk_usage(image_path)
    return str(free // (2**30)) + 'GB von ' + str(total // (2**30)) + 'GB'


def path_size(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')


def video_count(path):
    count = 0
    new_path, directories, files = next(os.walk(path))
    count += len(files)
    for directory in directories:
        count += video_count(path + '/' + directory)
    return count


def delete_old_files(path, delay):
    new_path, directories, files = next(os.walk(path))
    for file in files:
        age = time() - float(os.path.getmtime(path + '/' + file))
        age = age/3600/24
        if file.endswith('.jpg') and age > delay:
            os.remove(path + '/' + file)
    for directory in directories:
        delete_old_files(path + '/' + directory, delay)


def main():
    delete_old_files(image_path, delete_delay)


if __name__ == "__main__":
    main()
