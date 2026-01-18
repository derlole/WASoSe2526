import json

def extract_names(obj):
    """
    Rekursive Funktion, die alle Werte des Attributs 'name' aus einem JSON-Objekt sammelt.
    """
    names = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "name":
                names.append(value)
            else:
                names.extend(extract_names(value))
    elif isinstance(obj, list):
        for item in obj:
            names.extend(extract_names(item))

    return names

def extract_names_from_file(filename):
    """
    Liest eine JSON-Datei und gibt eine Liste aller 'name'-Werte zurück.
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return extract_names(data)

# Beispielnutzung
if __name__ == "__main__":
    filename = "example.json"  # Hier Pfad zur JSON-Datei anpassen
    names = extract_names_from_file(filename)
    print("Gefundene 'name'-Werte:")
    print(names)
