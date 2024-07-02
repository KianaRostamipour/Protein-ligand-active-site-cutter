import os
import shutil
import re
# Replace 'target_dir' with the appropriate protein name as needed.
base_directory = os.getcwd()
target_directory = os.path.join(base_directory, 'target_dir')
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

copied_dirs_count = 0
patterns = [
    re.compile(r'cut_(\d+)'),
    re.compile(r'lig'),
    re.compile(r'(\d+)_as')
]

for dir_name in os.listdir(base_directory):
    dir_path = os.path.join(base_directory, dir_name)
    if os.path.isdir(dir_path) and dir_name.isdigit():
        pdb_dir_name = f'pdb_{dir_name}'
        pdb_dir_path = os.path.join(dir_path, pdb_dir_name)
        if os.path.exists(pdb_dir_path):
            for subdir_name in os.listdir(pdb_dir_path):
                for pattern in patterns:
                    match = pattern.match(subdir_name)
                    if match:
                        num_part = match.group(2)
                        source_dir_path = os.path.join(pdb_dir_path, subdir_name)
                        target_num_dir_path = os.path.join(target_directory, f"target_dir")
                        if not os.path.exists(target_num_dir_path):
                            os.makedirs(target_num_dir_path)
                        target_subdir_path = os.path.join(target_num_dir_path, f"{dir_name}_{subdir_name}")
                        shutil.copytree(source_dir_path, target_subdir_path, dirs_exist_ok=True)
                        copied_dirs_count += 1
print(f"done")

