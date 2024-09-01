import os
import shutil
import csv

# Define source directories and destination path
source_game_dump = 'game_dump'
source_translations = 'translations'
destination_build = 'build'

# Function to copy folders
def copy_folder(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)  # Remove existing directory
    shutil.copytree(src, dest)
    print(f"Copied '{src}' to '{dest}'")

# Copy the game_dump/text folder to build/text
copy_folder(source_game_dump, destination_build)

# Define the base directories to search for CSV files
base_dirs = [destination_build, source_translations]

# Function to process each CSV file
def process_csv(file_path, base_dir):
    # Compute the relative path from the base directory
    relative_path = os.path.relpath(file_path, base_dir)
    # Compute the new path in the destination directory
    txt_file_path = os.path.join(destination_build, relative_path.replace('.csv', '.GMM.JAPANESE.txt'))

    # Ensure the directory for the text file exists
    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)

    # Open the CSV file
    with open(file_path, mode='r', encoding='utf-16') as csv_file:  # Adjust encoding if necessary
        csv_reader = csv.DictReader(csv_file)
        
        # Find the 'Translated' column (case-sensitive)
        fieldnames = csv_reader.fieldnames
        if 'Translated' not in fieldnames:
            print(f"Warning: 'Translated' column not found in {file_path}")
            return
        
        # Open the text file for writing
        with open(txt_file_path, mode='w', encoding='utf-8') as txt_file:
            for row in csv_reader:
                # Get the 'Translated' column value
                translated_text = row.get('Translated', '')
                txt_file.write(f"{translated_text}\n")

    print(f"Processed '{file_path}' and created '{txt_file_path}'")

# Recursively search for CSV files in both base directories and process each
for base_dir in base_dirs:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                process_csv(csv_file_path, base_dir)
