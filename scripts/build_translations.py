import os
import csv

def process_output_directory(output_directory, merged_csv_output):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(merged_csv_output), exist_ok=True)

    # Open the final merged CSV file
    with open(merged_csv_output, 'w', newline='', encoding='utf-16') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
        # Write header row for the merged CSV
        csvwriter.writerow(["filename", "text", "source", "skip"])
        
        # Walk through the output directory to find all CSV files
        for root, dirs, files in os.walk(output_directory):
            for file_name in files:
                if file_name.endswith('.csv'):
                    file_path = os.path.join(root, file_name)
                    print(f"Processing file: {file_path}")
                    
                    try:
                        # Open each individual CSV file
                        with open(file_path, 'r', encoding='utf-16') as csvfile_in:
                            csvreader = csv.reader(csvfile_in)
                            # Read header row
                            header = next(csvreader)
                            
                            # Determine indices for the columns
                            final_idx = header.index("Final") if "Final" in header else None
                            draft_idx = header.index("Draft") if "Draft" in header else None
                            cleaned_idx = header.index("Cleaned") if "Cleaned" in header else None
                            translated_idx = header.index("Translated") if "Translated" in header else None
                            source = ""

                            # Check indices for debugging
                            print(f"Header columns: {header}")
                            print(f"Indices - Final: {final_idx}, Draft: {draft_idx}, Cleaned: {cleaned_idx}, Translated: {translated_idx}")
                            
                            # Iterate through each row and extract the text based on priority
                            for line_num, row in enumerate(csvreader, start=1):
                                text = ''
                                if final_idx is not None and final_idx < len(row) and row[final_idx].strip():
                                    text = row[final_idx]
                                    source = "Final"
                                elif draft_idx is not None and draft_idx < len(row) and row[draft_idx].strip():
                                    text = row[draft_idx]
                                    source = "Draft"
                                elif cleaned_idx is not None and cleaned_idx < len(row) and row[cleaned_idx].strip():
                                    text = row[cleaned_idx]
                                    source = "Cleaned"
                                elif translated_idx is not None and translated_idx < len(row) and row[translated_idx].strip():
                                    text = row[translated_idx]
                                    source = "Translated"

                                if text:  # Only log if there is text
                                    # Write to the final merged CSV
                                    csvwriter.writerow([f"{file_path}:{line_num}", text, source])
                    
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

    print(f"Finished processing. Merged CSV created at: {merged_csv_output}")

# Usage
output_directory = './translations'  # Directory where your output CSVs are located
merged_csv_output = './tmp/merged_translated.csv'  # Path to the final CSV output

process_output_directory(output_directory, merged_csv_output)
