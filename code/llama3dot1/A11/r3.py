import json

def extract_names(file_path):
    """
    Extrahiere alle Werte des Attributs 'name' aus einer JSON-Datei.

    Args:
        file_path (str): Pfad zur JSON-Datei.

    Returns:
        list: Liste mit allen Namen.
    """

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            names = extract_names_recursive(data)
            return sorted(set(names))  # Entferne Duplikate und sortiere

    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
        return []
    except json.JSONDecodeError as e:
        print(f"Fehler bei der JSON-Parsung: {e}")
        return []

def extract_names_recursive(data):
    """
    Durchsucht die verschachtelte JSON-Struktur nach Werten des Attributs 'name'.

    Args:
        data (dict oder list): Die aktuelle JSON-Ebene.

    Returns:
        list: Liste mit allen Namen.
    """

    names = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'name':
                names.append(value)
            elif isinstance(value, (dict, list)):
                names.extend(extract_names_recursive(value))
    elif isinstance(data, list):
        for item in data:
            names.extend(extract_names_recursive(item))

    return names

# Beispielaufruf
file_path = 'path/to/your/json/file.json'
names = extract_names(file_path)
print(names)