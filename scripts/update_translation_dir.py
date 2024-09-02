import pandas as pd
import os

# Read the main output.csv file
output_csv = pd.read_csv('output.csv', encoding='utf-16')

# Define the columns to update in the translated files
columns_to_update = ['File', 'Japanese', 'Korean', 'Translated']

# Recursively search through the 'untranslated' directory for CSV files
translated_dir = './untranslated'

for root, dirs, files in os.walk(translated_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)

            # Open each found CSV file
            translated_csv = pd.read_csv(file_path, encoding='utf-16')

            # Ensure no leading/trailing whitespace in column names
            output_csv.columns = output_csv.columns.str.strip()
            translated_csv.columns = translated_csv.columns.str.strip()

            if 'File' not in translated_csv.columns:
                print(f"Error: 'File' column not found in {file_path}")
                continue

            # Merge by 'File' and update columns in the translated CSV
            for index, row in translated_csv.iterrows():
                file_value = row['File']

                # Find the matching row in the output_csv based on 'File'
                matching_row = output_csv[output_csv['File'] == file_value]

                if not matching_row.empty:
                    # Update the existing columns with the values from output_csv
                    translated_csv.at[index, 'Japanese'] = matching_row['Japanese'].values[0]
                    translated_csv.at[index, 'Korean'] = matching_row['Korean'].values[0]
                    translated_csv.at[index, 'Translated'] = matching_row['Translated'].values[0]

            # Save the updated CSV back
            translated_csv.to_csv(file_path, encoding='utf-16', index=False)

            print(f"Updated {file_path}")
