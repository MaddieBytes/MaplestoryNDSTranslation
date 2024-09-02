import os
import pandas as pd

# Directory to search for UTF-8 CSVs
search_dir = './untranslated'

# Recursively search for CSV files
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)

            # Try reading the file as UTF-8
            try:
                df = pd.read_csv(file_path, encoding='utf-8')

                # Convert and save the file as UTF-16
                df.to_csv(file_path, encoding='utf-16', index=False)

                print(f"Converted {file_path} to UTF-16")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
