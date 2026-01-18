import os

def create_and_read_file(file_path, content):
    try:
        # Erstellen und schreiben in die Datei
        with open(file_path, 'w') as file:
            file.write(content)
        
        # Abrufen der Dateigröße
        file_size = os.path.getsize(file_path)
        print(f"Dateigröße: {file_size} Byte")
        
        # Lesen und Ausgeben des Inhalts
        with open(file_path, 'r') as file:
            file_content = file.read()
            print("Dateiinhalt:")
            print(file_content)
    
    except IOError as e:
        print(f"Fehler beim Dateizugriff: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    file_path = "Beispiel.txt"
    content = "Dies ist ein Testinhalt für die Datei."
    
    create_and_read_file(file_path, content)