import csv
import language_tool_python
import re
from collections import defaultdict
from tqdm import tqdm

# Initialize the language tool
tool = language_tool_python.LanguageTool('en-US')
custom_dictionary_file = 'custom_dictionary.txt'

def load_custom_dictionary(file):
    with open(file, mode='r', newline='', encoding='utf-8') as infile:
        return set(line.strip() for line in infile)
    
def check_matches_against_custom_dictionary(custom_dictionary, matches):
    # Filter out matches that are in the custom dictionary
    for match in matches:
        for replacement in match.replacements:
            if replacement in custom_dictionary:
                matches.remove(match)
                break

def clean_text(text):
    # Remove square brackets their contents and 
    cleaned_text = re.sub(r'\[.*?\]', ' ', text)
    # Removed Japanese quotation marks
    cleaned_text = re.sub(r'「|」', '', cleaned_text)
    cleaned_text = re.sub(r'『|』', '', cleaned_text)

    # if there are now two spaces, replace with one space
    cleaned_text = re.sub(r'  ', ' ', cleaned_text)

    # Remove player references \[name:*_PC\] and a trailing space
    cleaned_text = re.sub(r'\[name:*_PC\] ', '', cleaned_text)
    

    return cleaned_text

def check_text(text):
    # Check the text using language_tool_python
    matches = tool.check(text)
    return matches

def apply_corrections(text, matches):
    # Apply corrections to the text based on the matches
    return language_tool_python.utils.correct(text, matches)

def main(input_csv, output_log):
    # Load custom dictionary
    custom_dictionary = load_custom_dictionary(custom_dictionary_file)
    issue_counts = defaultdict(int)
    
    # Count total rows for tqdm
    with open(input_csv, mode='r', newline='', encoding='utf-16') as infile:
        total_rows = sum(1 for _ in infile)
    
    with open(input_csv, mode='r', newline='', encoding='utf-16') as infile, \
         open(output_log, mode='w', newline='', encoding='utf-8') as logfile:
        
        reader = csv.DictReader(infile)
        log_writer = csv.writer(logfile)
        
        # Write headers to log file
        log_writer.writerow(['Filename', 'Original Text', 'Sanitized Text', 'Issue', 'Suggested Correction', 'Recommended Change'])
        
        # Initialize tqdm with total row count
        progress_bar = tqdm(reader, total=total_rows - 1, desc="Processing Rows")
        
        for row_num, row in enumerate(progress_bar, start=1):
            filename = row['filename']  # Use the 'filename' column
            text = row['text']  # Assuming the column with the text is named 'text'
            unsanitized_text = text  # Save the original text
            cleaned_text = clean_text(text)
            matches = check_text(cleaned_text)
            matches = check_matches_against_custom_dictionary(custom_dictionary, matches)
            
            if matches:
                # Process only the first match
                match = matches[0]
                
                # Apply corrections to get recommended change
                recommended_change = apply_corrections(cleaned_text, matches)
                
                # Extract suggested corrections and limit the length
                suggested_corrections = ', '.join(replacement for replacement in match.replacements[:5])
                
                # Log the details
                log_writer.writerow([filename, unsanitized_text, cleaned_text, match.message, suggested_corrections, recommended_change])
                issue_counts[match.message] += 1
                    
            # Update progress bar description
            progress_bar.set_description(f"Processing Rows ({row_num}/{total_rows - 1})")
                    
    # Print summary of issues
    print("Summary of Issues:")
    for issue, count in issue_counts.items():
        print(f"{issue}: {count} occurrences")
    print(f"Issues logged to {output_log}")

if __name__ == "__main__":
    input_csv = 'tmp/merged_translated.csv'
    output_log = 'tmp/issue_summary.csv'
    main(input_csv, output_log)
