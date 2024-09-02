import csv
import os

# Directory paths
csv_directory = 'untranslated'
compiled_directory = 'compiled'

# Function to remove double backslashes
def remove_double_backslashes(text):
    return text.replace('\\\\', '\\')

# Function to update the specific line in the file
def update_line_in_file(file_path, line_number, new_content):
    # Read the existing content
    with open(file_path, 'r', encoding='utf-16') as file:
        lines = file.readlines()

    # Update the specified line
    if 0 <= line_number < len(lines):
        lines[line_number] = new_content + '\n'
    else:
        print(f"Line number {line_number} is out of range in file {file_path}")

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-16') as file:
        file.writelines(lines)

# Recursively search for CSV files and process them
for root, dirs, files in os.walk(csv_directory):
    for file_name in files:
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(root, file_name)
            
            with open(csv_file_path, 'r', encoding='utf-16') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    file_info = row['File']
                    final_draft = row.get('FinalDraft', '').strip()
                    cleaned = row.get('Cleaned', '').strip()
                    translated = row.get('Translated', '').strip()
                    
                    # Prefer FinalDraft over Cleaned, and Cleaned over Translated
                    if final_draft:
                        text_to_use = final_draft
                    elif cleaned:
                        text_to_use = cleaned
                    else:
                        text_to_use = translated
                    
                    # Remove double backslashes
                    cleaned_text = remove_double_backslashes(text_to_use)

                    # Split the file_info into filename and line number
                    filename, line_number_str = file_info.split(':')
                    line_number = int(line_number_str) - 1  # Convert to 0-based index

                    # Add .JAPANESE before the file extension
                    base_name, ext = os.path.splitext(filename)
                    modified_filename = f"{base_name}.JAPANESE{ext}"
                    print(f"Updating {modified_filename} at line {line_number}")
                    
                    # Construct the file path in the compiled directory
                    file_path = os.path.join(compiled_directory, modified_filename)

                    # Ensure the file exists in the compiled directory before updating
                    if os.path.exists(file_path):
                        update_line_in_file(file_path, line_number, cleaned_text)
                    else:
                        print(f"File {file_path} does not exist")
