import json

def extract_names(file_path):
    # Funktion, die rekursiv nach Namen sucht
    def find_names(data):
        names = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'name':
                    names.append(value)
                elif isinstance(value, (dict, list)):
                    names.extend(find_names(value))
        elif isinstance(data, list):
            for item in data:
                names.extend(find_names(item))
        return names

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return find_names(data)
        except json.JSONDecodeError as e:
            print("Fehler beim Parsen der JSON-Datei:", e)
            return []

# Beispiel-Verwendung
file_path = 'example.json'  # Ersetzen Sie dies mit dem Pfad zu Ihrer JSON-Datei
names = extract_names(file_path)
print(names)