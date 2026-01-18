import json

def extract_names(json_data):
    """
    Recursively extracts all values associated with the key 'name' from the given JSON data.
    
    :param json_data: A dictionary or list representing the JSON structure
    :return: A list of names found in the JSON data
    """
    names = []
    
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == 'name':
                names.append(value)
            elif isinstance(value, (dict, list)):
                names.extend(extract_names(value))
    elif isinstance(json_data, list):
        for item in json_data:
            names.extend(extract_names(item))
    
    return names

def read_and_extract_names(file_path):
    """
    Reads a JSON file and extracts all values associated with the key 'name'.
    
    :param file_path: The path to the JSON file
    :return: A list of names found in the JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return extract_names(json_data)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")

# Example usage
if __name__ == "__main__":
    # Assuming 'data.json' is a valid JSON file in the same directory as this script
    names = read_and_extract_names('data.json')
    if names is not None:
        print("Names extracted from JSON:", names)