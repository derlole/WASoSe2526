import json

def extract_names_from_json(json_file_path):
    def extract_names(data):
        names = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'name':
                    names.append(value)
                elif isinstance(value, (dict, list)):
                    names.extend(extract_names(value))
        elif isinstance(data, list):
            for item in data:
                names.extend(extract_names(item))
        return names

    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    return extract_names(json_data)

# Example usage:
# Assuming you have a JSON file named "data.json"
json_file_path = 'path/to/your/data.json'
names = extract_names_from_json(json_file_path)
print(names)