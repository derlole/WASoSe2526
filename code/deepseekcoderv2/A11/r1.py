import json

def extract_names(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    def find_names(obj):
        names = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "name":
                    names.append(value)
                elif isinstance(value, (dict, list)):
                    names.extend(find_names(value))
        elif isinstance(obj, list):
            for item in obj:
                names.extend(find_names(item))
        return names
    
    return find_names(data)

# Beispielaufruf
json_file = 'example.json'
names = extract_names(json_file)
print(names)