import os

def erstelle_datei(inhalt):
    """
    Erstellt eine neue Datei mit dem angegebenen Inhalt.

    Args:
        inhalt (str): Der Inhalt der neuen Datei.
    """
    dateiname = "meine_datei.txt"  # Benutzer definierte Dateinamen sind besser, aber für dieses Beispiel reicht's
    try:
        with open(dateiname, 'w') as datei:
            datei.write(inhalt)
        print(f"Datei '{dateiname}' erfolgreich erstellt.")
    except Exception as e:
        print(f"Fehler beim Erstellen der Datei: {e}")

def lese_datei_inhalt():
    """
    Liest den Inhalt einer vorherigen angelegten Datei.

    Returns:
        str: Der Inhalt der Datei.
    """
    dateiname = "meine_datei.txt"
    try:
        with open(dateiname, 'r') as datei:
            return datei.read()
    except FileNotFoundError:
        print(f"Datei '{dateiname}' nicht gefunden.")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen des Inhalts: {e}")
        return None

def berechne_dateigröße(inhalt):
    """
    Berechnet die Größe einer Zeichenkette.

    Args:
        inhalt (str): Die Zeichenkette, deren Größe ermittelt werden soll.

    Returns:
        int: Die Größe der Zeichenkette.
    """
    return len(inhalt)

def main():
    inhalt = "Dies ist ein Testinhalts der Datei."
    erstelle_datei(inhalt)
    datei_inhalt = lese_datei_inhalt()
    if datei_inhalt is not None:
        dateigröße = berechne_dateigröße(datei_inhalt)
        print(f"Inhalt: \n{datei_inhalt}")
        print(f"Dateigröße: {dateigröße} Zeichen")

if __name__ == "__main__":
    main()