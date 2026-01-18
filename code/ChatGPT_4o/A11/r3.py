import json

def extract_names(data):
    """
    Rekursive Funktion, die alle Werte des Attributs 'name' aus einem JSON-Objekt extrahiert.
    data: kann ein dict, list oder primitive Daten sein
    Rückgabe: Liste aller gefundenen 'name'-Werte
    """
    names = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "name":
                names.append(value)
            else:
                # Rekursiv durchsuchen
                names.extend(extract_names(value))
    elif isinstance(data, list):
        for item in data:
            names.extend(extract_names(item))
    # Bei primitiven Typen nichts tun
    return names

def extract_names_from_file(file_path):
    """
    Liest eine JSON-Datei und extrahiert alle 'name'-Werte
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return extract_names(data)

# --- Beispielhafte Nutzung ---
if __name__ == "__main__":
    file_path = "example.json"  # Pfad zu deiner JSON-Datei
    all_names = extract_names_from_file(file_path)
    print("Gefundene 'name'-Werte:", all_names)
