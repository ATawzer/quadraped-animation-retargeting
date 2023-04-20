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

    # Get a list of all the files in directory1
    files = os.listdir(dir1)

    # Loop through each file and copy it to directory2
    for file in files:
        # Construct full file paths
        src_file = os.path.join(dir1, file)
        dest_file = os.path.join(dir2, file)
        # Copy file to directory2
        shutil.copy(src_file, dest_file)

    # Create a zip file with the same name as the last part of dir2
    zip_name = os.path.basename(dir1)
    zip_file = zipfile.ZipFile(zip_name + '.zip', 'w')

    # Add all files in dir2 to the zip file
    for file in os.listdir(dir1):
        file_path = os.path.join(dir1, file)
        zip_file.write(file_path, file)

    # Close the zip file
    zip_file.close()