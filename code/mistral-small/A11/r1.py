import json

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

def main():
    # Lese die JSON-Datei
    with open('path/to/your/file.json', 'r') as file:
        data = json.load(file)

    # Extrahiere alle Namen
    names = extract_names(data)

    # Gib die extrahierten Namen aus
    print(names)

if __name__ == "__main__":
    main()