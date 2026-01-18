import os

def create_and_display_file(filename):
    # Beispielinhalt für die Datei
    content = "Dies ist der Inhalt der erstellten Datei."
    
    try:
        # Datei öffnen oder erstellen (w)
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Datei '{filename}' wurde erstellt.")
        
        # Dateigröße ermitteln
        size = os.path.getsize(filename)
        print(f"Die Dateigröße von '{filename}' beträgt {size} Bytes.")
        
        # Inhalt der Datei lesen und ausgeben
        with open(filename, 'r') as file:
            content = file.read()
            print("Inhalt der Datei:")
            print(content)
    
    except IOError as e:
        print(f"Es ist ein Fehler beim Arbeiten mit der Datei aufgetreten: {e}")

# Beispielaufruf des Programms
create_and_display_file('example.txt')