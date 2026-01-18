import os

def create_and_display_file(filename):
    # Text, den wir in die Datei schreiben möchten
    content = "Dies ist der Inhalt der Datei."

    try:
        # Datei erstellen und mit dem angegebenen Inhalt schreiben
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Die Datei '{filename}' wurde erstellt.")

        # Dateigröße ermitteln und ausgeben
        size = os.path.getsize(filename)
        print(f"Die Dateigröße von '{filename}' beträgt {size} Bytes.")

        # Dateiinhalt anzeigen
        with open(filename, 'r') as file:
            content = file.read()
            print("Inhalt der Datei:")
            print(content)

    except IOError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Namen der zu erstellenden Datei
filename = "example.txt"

# Funktion aufrufen
create_and_display_file(filename)