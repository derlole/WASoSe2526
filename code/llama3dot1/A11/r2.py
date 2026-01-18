import json

def extrahiere_name_atribut(json_datei):
    """
    Extrahiert alle Werte des Attributs "name" aus einer JSON-Datei.

    Args:
        json_datei (str): Der Inhalt der JSON-Datei als String.

    Returns:
        list: Eine Liste mit allen Namen.
    """
    # Die JSON-Daten in ein Python-Objekt parsen
    data = json.loads(json_datei)

    # Eine Funktion definieren, die in verschachtelten Strukturen nach "name" sucht
    def such_name(obj):
        if isinstance(obj, dict):
            return obj.get('name') or [such_name(value) for value in obj.values() if isinstance(value, (dict, list))][0]
        elif isinstance(obj, list):
            return [such_name(item) for item in obj if isinstance(item, (dict, list))]
        else:
            return None

    # Die Funktion auf das gesamte Datenobjekt anwenden und die Ergebnisse sammeln
    name_atribut_werte = []
    such_name(data, name_atribut_werte.append)

    return name_atribut_werte

# Beispiel-Aufruf:
json_datei_inhalt = '''
{
    "name": "Mein Name",
    "adresse": {
        "straße": "Hauptstraße 1",
        "hausnummer": 123,
        "stadt": "Berlin"
    },
    "freunde": [
        {"name": "Max", "alter": 25},
        {"name": "Lisa", "alter": 30}
    ]
}
'''

print(extrahiere_name_atribut(json_datei_inhalt))