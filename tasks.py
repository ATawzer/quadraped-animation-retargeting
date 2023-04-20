from invoke import task

import os
import shutil
import zipfile

@task
def update(c, blender_version="3.5"):
    """
    Installs the latest version of the addon to the default Blender addons directory
    """
    user_dir = os.path.expanduser('~')

    # Set directory paths
    dir1 = './qar'
    dir2 = f"{user_dir}/AppData/Roaming/Blender Foundation/Blender/{blender_version}/scripts/addons/qar"

    if os.path.exists(dir2):
        shutil.rmtree(dir2)

    # Loop through each file and copy it to directory2
    shutil.copytree(dir1, dir2)

@task
def zip(c):
    """
    Creates a zip file of the addon
    """

    dir1 = './qar'

    # Create a zip file with the same name as the last part of dir1
    zip_name = os.path.basename(dir1)
    with zipfile.ZipFile(zip_name + '.zip', 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk(dir1):
            for filename in filenames:
                # Create the full filepath by using os.path.join()
                filepath = os.path.join(foldername, filename)
                # Add the file to the zip file
                zip_file.write(filepath, os.path.relpath(filepath, dir1))