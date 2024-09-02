import os
import re

# Define a more flexible regex pattern to match Lua function definitions
function_pattern = re.compile(r'\b(\w+)\s*\(([^)]*)\)', re.MULTILINE)

def extract_lua_functions_from_file(file_path):
    functions = []
    try:
        with open(file_path, 'r', encoding='utf-16') as file:
            content = file.read()
            matches = function_pattern.findall(content)
            for match in matches:
                function_name, params = match
                functions.append((function_name, params))
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return functions

def extract_lua_functions_from_directory(directory_path):
    all_functions = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                functions = extract_lua_functions_from_file(file_path)
                all_functions.extend(functions)
    return all_functions

def main(directory_path):
    functions = extract_lua_functions_from_directory(directory_path)
    if not functions:
        print("No functions found.")
    for function_name, params in functions:
        print(f"Function Name: {function_name}, Parameters: {params}")

# Replace 'your_directory_path' with the path to the directory you want to scan
if __name__ == '__main__':
    main('game_dump')
