import json

def extract_names(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    def find_names(node):
        names = []
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "name":
                    names.append(value)
                else:
                    names.extend(find_names(value))
        elif isinstance(node, list):
            for item in node:
                names.extend(find_names(item))
        return names
    
    return find_names(data)

# Beispielaufruf
file_path = 'example.json'  # Pfad zur JSON-Datei
names = extract_names(file_path)
print(names)