import os

def main():
    dateiname = "beispiel.txt"
    inhalt = "Hallo Welt!\nDies ist eine Testdatei.\n"

    try:
        # Datei erstellen und schreiben
        with open(dateiname, "w", encoding="utf-8") as datei:
            datei.write(inhalt)
        print(f"Datei '{dateiname}' erfolgreich erstellt.")

        # Dateigröße ermitteln
        groesse = os.path.getsize(dateiname)
        print(f"Dateigröße: {groesse} Bytes")

        # Dateiinhalt auslesen und anzeigen
        with open(dateiname, "r", encoding="utf-8") as datei:
            gelesener_inhalt = datei.read()
        print("Dateiinhalt:")
        print(gelesener_inhalt)

    except OSError as e:
        print(f"Fehler beim Zugriff auf die Datei: {e}")

if __name__ == "__main__":
    main()
