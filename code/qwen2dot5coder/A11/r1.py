import json

def extract_names_from_json(file_path):
    def extract_names(obj):
        names = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "name":
                    names.append(value)
                elif isinstance(value, (dict, list)):
                    names.extend(extract_names(value))
        elif isinstance(obj, list):
            for item in obj:
                names.extend(extract_names(item))
        return names

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return extract_names(data)

# Example usage
if __name__ == "__main__":
    file_path = 'path_to_your_json_file.json'
    names = extract_names_from_json(file_path)
    print(names)