import os
import csv
import re

def extract_info_from_filename(filename):
    """Extract the base value and language from the filename."""
    match = re.match(r'^([A-Za-z0-9_]+)\.GMM\.(KOREAN|JAPANESE|TRANSLATED)\.txt$', filename)
    if match:
        base_value = match.group(1)  # xxxxxx part of the filename
        language = match.group(2)  # KOREAN, JAPANESE, or TRANSLATED
        return base_value, language
    else:
        # Handle files like 28.GMM.txt assuming they are Japanese
        match_simple = re.match(r'^([0-9]+)\.GMM\.txt$', filename)
        if match_simple:
            base_value = match_simple.group(1)  # xxxxxx part of the filename
            return base_value, "JAPANESE"
    return None, None

def read_file_lines(file_path):
    """Read all lines from a file."""
    with open(file_path, 'r', encoding='utf-16') as file:
        return file.readlines()

def process_files(input_directory, output_directory):
    """Process all files in the input directory and create corresponding CSV files."""
    # Dictionary to hold content for each base filename and its directory
    file_data = {}

    # Walk through the directory
    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith('.txt'):
                base_value, language = extract_info_from_filename(file_name)
                
                if base_value:
                    file_path = os.path.join(root, file_name)
                    lines = read_file_lines(file_path)
                    
                    # Store the directory path relative to the input_directory
                    relative_dir = os.path.relpath(root, input_directory)

                    # Initialize the entry if it doesn't exist
                    if base_value not in file_data:
                        file_data[base_value] = {
                            'directory': relative_dir,
                            'korean': [],
                            'japanese': [],
                            'translation': []
                        }

                    # Append each line to the correct language list
                    for line_content in lines:
                        line_content = line_content.strip()
                        
                        if language == "KOREAN":
                            file_data[base_value]['korean'].append(line_content)
                        elif language == "JAPANESE":
                            file_data[base_value]['japanese'].append(line_content)
                        elif language == "TRANSLATED":
                            file_data[base_value]['translation'].append(line_content)
    # Now create CSV files for each base filename in the corresponding output directory
    for base_value, data in file_data.items():
        # Reconstruct the output directory path based on the original directory structure
        output_dir = create_directory_structure(output_directory, data['directory'])
        output_csv = os.path.join(output_dir, f'{base_value}.csv')
        
        # Write to CSV
        with open(output_csv, 'w', newline='', encoding='utf-16') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
            # Write the header row
            csvwriter.writerow(["Korean", "Japanese", "K->Machine", "J->Machine", "Translated", "Cleaned", "Draft", "Final", "Notes", "Skip Formatting Check"])
            
            # Determine the maximum number of lines across the three languages
            max_lines = max(len(data['korean']), len(data['japanese']), len(data['translation']))

            # Write each row in the CSV
            for i in range(max_lines):
                korean_entry = data['korean'][i] if i < len(data['korean']) else ''
                japanese_entry = data['japanese'][i] if i < len(data['japanese']) else ''
                translation_entry = data['translation'][i] if i < len(data['translation']) else ''
                
                csvwriter.writerow([
                    korean_entry,  # Korean text for that line (if any)
                    japanese_entry,  # Japanese text for that line (if any)
                    '',  # Machine translation from Korean to Japanese
                    '',  # Machine translation from Japanese to Korean
                    translation_entry,  # Translation text for that line (if any)
                    '',  # Cleaned text
                    '',  # Draft text
                    '',  # Final text
                    '',  # Notes
                    ''  # Skip formatting check
                ])

def create_directory_structure(output_root, relative_path):
    """Create the directory structure in the output folder."""
    output_dir = os.path.join(output_root, relative_path)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Usage
input_directory = 'game_dump'  # Directory where your input files are stored
output_directory = 'translations'  # Root directory where the CSV files will be saved
process_files(input_directory, output_directory)
