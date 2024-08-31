import os
import re
import csv
import argparse

# Function to find text between {} in a single file
def find_text_between_brackets(file_path, pattern):
    found_texts = set()
    with open(file_path, 'r', encoding='utf-16', errors='ignore') as file:
        content = file.read()
        matches = re.findall(pattern, content)
        found_texts.update(matches)
    return found_texts

# Function to find Korean text in a single file
def find_korean_text(file_path, pattern):
    found_texts = set()
    with open(file_path, 'r', encoding='utf-16', errors='ignore') as file:
        content = file.read()
        matches = re.findall(pattern, content)
        found_texts.update(matches)
    return found_texts

# Function to recursively search directory
def search_directory(directory, pattern_brackets, pattern_korean):
    combined_texts = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.txt'):  # Only process .txt files
                bracket_texts = find_text_between_brackets(file_path, pattern_brackets)
                korean_texts = find_korean_text(file_path, pattern_korean)
                combined_texts.update(bracket_texts)
                combined_texts.update(korean_texts)
    return combined_texts

# Function to write results to a CSV file
def write_to_csv(texts, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure the output directory exists
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Unique Text'])  # Header
        for text in texts:
            writer.writerow([text])

# Main function
def main(args):
    pattern_brackets = r'{(.*?)}'  # Regex pattern to match text between {}
    pattern_korean = r'[가-힣]+'  # Regex pattern to match Korean characters
    unique_texts = search_directory(args.input_dir, pattern_brackets, pattern_korean)
    write_to_csv(unique_texts, args.output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search for specific texts and output to a CSV file.')
    parser.add_argument('--input-dir', type=str, default='./text', help='Directory to search for text files.')
    parser.add_argument('--output-file', type=str, default='./results/nouns.csv', help='CSV file to write results.')

    args = parser.parse_args()
    main(args)
