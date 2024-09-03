import os
import re

def rename_files_in_directory(root_dir):
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if 'TRANSLATED' is in the filename
            if 'TRANSLATED' in filename:
                # Construct old and new file paths
                old_file_path = os.path.join(dirpath, filename)
                new_filename = filename.replace('TRANSLATED', 'JAPANESE')
                new_file_path = os.path.join(dirpath, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')

# Set the root directory path
root_directory = 'compiled'

# Call the function to rename files
rename_files_in_directory(root_directory)
