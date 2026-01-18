import json

def extract_names(data):
    """
    Rekursive Funktion, um alle Werte des Attributs 'name' aus beliebig
    verschachtelten JSON-Strukturen zu extrahieren.
    """
    names = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "name":
                names.append(value)
            else:
                names.extend(extract_names(value))
    elif isinstance(data, list):
        for item in data:
            names.extend(extract_names(item))

    return names

def read_json_and_extract_names(file_path):
    """
    Liest eine JSON-Datei ein und extrahiert alle 'name'-Werte.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return extract_names(data)

# Beispielaufruf
if __name__ == "__main__":
    file_path = "beispiel.json"  # Pfad zur JSON-Datei
    names_list = read_json_and_extract_names(file_path)
    print("Gefundene Namen:", names_list)
