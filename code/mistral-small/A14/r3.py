import os

def create_and_display_file(filename, content):
    try:
        # Erstellen der Datei und Schreiben des Inhalts
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Datei '{filename}' erfolgreich erstellt.")

        # Ermitteln der Dateigröße
        file_size = os.path.getsize(filename)
        print(f"Größe der Datei '{filename}': {file_size} Bytes")

        # Lesen und Anzeigen des Inhalts
        with open(filename, 'r') as file:
            content = file.read()
        print(f"Inhalt der Datei '{filename}':\n{content}")

    except FileNotFoundError:
        print(f"Die Datei '{filename}' konnte nicht gefunden werden.")
    except PermissionError:
        print(f"Zugriff auf die Datei '{filename}' ist nicht erlaubt.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispiel-Inhalt für die Datei
content = "Das ist ein Beispieltext für die Datei."
filename = "beispiel.txt"

# Aufruf der Funktion
create_and_display_file(filename, content)