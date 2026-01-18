import os

def main():
    dateiname = "beispiel.txt"
    inhalt = "Hallo Welt!\nDies ist eine Testdatei.\nPython macht Dateimanagement einfach."

    try:
        # Datei erstellen und Inhalte schreiben
        with open(dateiname, "w", encoding="utf-8") as datei:
            datei.write(inhalt)
        print(f"Datei '{dateiname}' erfolgreich erstellt.")

        # Dateigröße ermitteln
        dateigroesse = os.path.getsize(dateiname)
        print(f"Dateigröße: {dateigroesse} Bytes")

        # Dateiinhalt lesen und anzeigen
        with open(dateiname, "r", encoding="utf-8") as datei:
            gelesener_inhalt = datei.read()
        print("\nDateiinhalt:\n----------------")
        print(gelesener_inhalt)
        print("----------------")

    except OSError as e:
        print(f"Fehler beim Zugriff auf die Datei: {e}")

if __name__ == "__main__":
    main()
