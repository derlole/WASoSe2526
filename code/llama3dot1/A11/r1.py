import json

def extrahiere_name(json_datei):
    """
    Extrahiert alle Werte des Attributs "name" aus einer JSON-Datei.

    :param json_datei: Pfad zur JSON-Datei
    :return: Liste von Namen
    """
    try:
        with open(json_datei, 'r') as dateihandle:
            data = json.load(dateihandle)
            namen = []
            extrahiere_namen(data, namen)
            return namen

    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden.")
    except json.JSONDecodeError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    except Exception as e:
        print(f"Ein unbekannter Fehler ist aufgetreten: {e}")

def extrahiere_namen(data, namen):
    """
    Durchsucht die verschachtelten Strukturen in der JSON-Datenstruktur nach Werten des Attributs "name".

    :param data: Die JSON-Datenstruktur
    :param namen: Liste von Namen (wird erweitert)
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'name':
                namen.append(value)
            elif isinstance(value, (dict, list)):
                extrahiere_namen(value, namen)

    elif isinstance(data, list):
        for item in data:
            extrahiere_namen(item, namen)


# Beispiel
json_datei = 'data.json'
namen = extrahiere_name(json_datei)
print(namen)