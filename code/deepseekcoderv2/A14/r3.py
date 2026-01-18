import os

def create_and_display_file(filename, content):
    try:
        # Schreibe den Inhalt in die Datei
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Datei '{filename}' wurde erstellt.")
        
        # Ermittle und gebe die Größe der Datei aus
        file_size = os.path.getsize(filename)
        print(f"Die Dateigröße von '{filename}' beträgt {file_size} Bytes.")
        
        # Gebe den Inhalt der Datei aus
        with open(filename, 'r') as file:
            content = file.read()
            print("Inhalt der Datei:")
            print(content)
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispielaufruf des Funktions mit einem Namen und Inhalt
create_and_display_file('example.txt', 'Das ist ein Testtext.')