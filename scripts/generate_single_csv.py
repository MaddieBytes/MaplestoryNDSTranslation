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

def process_files(input_directory, output_csv):
    """Process all files in the input directory and create a single CSV file."""
    # Dictionary to store lines from each file, grouped by the base filename
    file_data = {}

    # Walk through the directory and collect the lines based on language
    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith('.txt'):
                base_value, language = extract_info_from_filename(file_name)
                
                if base_value:
                    file_path = os.path.join(root, file_name)
                    lines = read_file_lines(file_path)

                    # Calculate the relative directory path
                    relative_dir = os.path.relpath(root, input_directory)

                    # Initialize entry if not present
                    if base_value not in file_data:
                        file_data[base_value] = {'korean': [], 'japanese': [], 'translated': [], 'directory': relative_dir}

                    # Store lines based on language
                    for line_content in lines:
                        line_content = line_content.strip()
                        
                        if language == "KOREAN":
                            file_data[base_value]['korean'].append(line_content)
                        elif language == "JAPANESE":
                            file_data[base_value]['japanese'].append(line_content)
                        elif language == "TRANSLATED":
                            file_data[base_value]['translated'].append(line_content)

    # Now write the combined data to a single CSV file
    with open(output_csv, 'w', newline='', encoding='utf-16') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
        # Write the header row
        csvwriter.writerow(["File", "Japanese", "Korean", "Translated"])

        # Iterate through the collected data and write rows to CSV
        for base_value, data in file_data.items():
            max_lines = max(len(data['korean']), len(data['japanese']), len(data['translated']))

            # Write each row with individual language lines
            for i in range(max_lines):
                japanese_entry = data['japanese'][i] if i < len(data['japanese']) else ''
                korean_entry = data['korean'][i] if i < len(data['korean']) else ''
                translation_entry = data['translated'][i] if i < len(data['translated']) else ''
                
                # Construct the directory/filename:line_number format
                filename_line = f"{data['directory']}/{base_value}.GMM.txt:{i+1}"
                
                # Write to CSV with columns: file, Japanese, Korean, Translated
                csvwriter.writerow([filename_line, japanese_entry, korean_entry, translation_entry])

# Usage
input_directory = 'game_dump'  # Directory where your input files are stored
output_csv = 'output.csv'  # Path to the output CSV file
process_files(input_directory, output_csv)
