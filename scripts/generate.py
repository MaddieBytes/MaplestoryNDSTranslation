import os
import csv
import requests
import json
import time
import argparse

# Rate limit settings
REQUESTS_PER_SECOND = 20  # Adjust to a realistic value
DELAY = 1 / REQUESTS_PER_SECOND  # Delay between requests

# Retry settings
MAX_RETRIES = 60  # Number of retries
RETRY_DELAY = 10  # Seconds to wait between retries

def translate_text(api_url, text, target_lang='en', source_lang='ko'):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(
                url=f"{api_url}/",
                json={
                    'target_lang': target_lang,
                    'text': [text],
                    'source_lang': source_lang
                }
            )
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            response_data = response.json()

            # Adjust according to the actual structure of the response
            return response_data[0]  # Adjust if needed based on actual response

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            retries += 1
            print(f"Retrying... ({retries}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

        except requests.exceptions.RequestException as req_err:
            print(f"Request exception occurred: {req_err}")
            retries += 1
            print(f"Retrying... ({retries}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            print(f"Translation error: {e}")
            retries += 1
            print(f"Retrying... ({retries}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

    raise SystemExit("Stopping script after max retries due to failed translation request.")

def get_processed_files(log_file_path):
    processed_files = {}
    if os.path.exists(log_file_path):
        with open(log_file_path, mode='r', encoding='utf-8') as log_file:
            for line in log_file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    file_path, line_number = parts
                    processed_files[file_path] = int(line_number)
    return processed_files

def find_all_txt_files(directory):
    """Recursively find all .txt files in the directory."""
    txt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

def get_unprocessed_files(all_txt_files, processed_files):
    """Filter out already processed files."""
    unprocessed_files = []
    for file in all_txt_files:
        if file not in processed_files or processed_files[file] == 0:
            unprocessed_files.append(file)
    return unprocessed_files

def process_file(file_path, output_directory, start_line, log_file_path, api_url):
    try:
        # Construct the output path
        relative_path = os.path.relpath(file_path, directory_to_search)
        output_path = os.path.join(output_directory, os.path.splitext(relative_path)[0] + '.csv')

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Open the CSV file for writing with UTF-16 encoding
        with open(output_path, mode='a', newline='', encoding='utf-16') as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)

            # Write headers if the file is newly created
            if os.path.getsize(output_path) == 0:
                writer.writerow(['Line Number', 'Line Content', 'Translation', 'Proofread', 'Notes'])

            # Track time for rate limiting
            last_request_time = time.time()

            # Read the contents of the text file line by line using UTF-16 encoding
            with open(file_path, 'r', encoding='utf-16') as txt_file:
                # Initialize line_number variable to avoid reference before assignment
                line_number = start_line

                # Skip lines until reaching the start_line
                for line_number, line in enumerate(txt_file, start=1):
                    if line_number <= start_line:
                        continue

                    line_content = line.strip()

                    # Enforce rate limiting
                    current_time = time.time()
                    elapsed_time = current_time - last_request_time
                    if elapsed_time < DELAY:
                        time.sleep(DELAY - elapsed_time)
                    last_request_time = time.time()

                    # Translate the line content with retry logic
                    translation = translate_text(api_url, line_content)

                    # Write the line to the CSV file with empty Proofread and Notes columns
                    writer.writerow([line_number, line_content, translation, '', ''])

                    print(f"Processed line {line_number} in file {file_path}")

        # Log the last processed line number after successfully processing the file
        with open(log_file_path, mode='a', encoding='utf-8') as log_file:
            log_file.write(f"{file_path}|{line_number}\n")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        raise SystemExit("Stopping script due to file read or write error.")

def process_all_files(directory, output_directory, log_file_path, api_url):
    # Get all .txt files recursively
    all_txt_files = find_all_txt_files(directory)

    # Get the list of already processed files
    processed_files = get_processed_files(log_file_path)
    print(f"Found {len(processed_files)} processed files.")

    # Filter out already processed files
    unprocessed_files = get_unprocessed_files(all_txt_files, processed_files)
    print(f"Found {len(unprocessed_files)} unprocessed files.")

    if not unprocessed_files:
        print("No unprocessed files found.")
        return

    # Process all unprocessed files
    for file_path in unprocessed_files:
        start_line = processed_files.get(file_path, 0)
        process_file(file_path, output_directory, start_line, log_file_path, api_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process .txt files for translation.')
    parser.add_argument('--apiurl', type=str, required=True, help='FastAPI endpoint URL')
    parser.add_argument('--input-dir', type=str, required=True, help='Directory to search for .txt files')
    parser.add_argument('--output-dir', type=str, required=True, help='Directory to save CSV files')
    parser.add_argument('--log-file', type=str, required=True, help='Log file path to track processed files')

    args = parser.parse_args()

    process_all_files(args.input_dir, args.output_dir, args.log_file, args.apiurl)

    print(f"Data saved to {args.output_dir} and log updated at {args.log_file}")
