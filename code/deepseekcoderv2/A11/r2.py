import json

def extract_names(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    def find_names(obj):
        names = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "name":
                    names.append(value)
                else:
                    names.extend(find_names(value))
        elif isinstance(obj, list):
            for item in obj:
                names.extend(find_names(item))
        return names
    
    return find_names(data)

# Beispielaufruf
file_path = 'pfad/zu/deiner/json-datei.json'
names = extract_names(file_path)
print(names)