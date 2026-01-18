import os

def create_file(filename, content):
    """
    Erstellt eine Datei mit dem angegebenen Inhalt.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Datei '{filename}' erfolgreich erstellt.")
    except IOError as e:
        print(f"Fehler beim Erstellen der Datei: {e}")
        return False
    return True

def get_file_size(filename):
    """
    Gibt die Größe der Datei in Bytes zurück.
    """
    try:
        size = os.path.getsize(filename)
        return size
    except OSError as e:
        print(f"Fehler beim Ermitteln der Dateigröße: {e}")
        return None

def read_file_content(filename):
    """
    Liest und gibt den Inhalt der Datei zurück.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except IOError as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None

def main():
    filename = "beispiel.txt"
    content = "Hallo Welt!\nDies ist ein Testinhalt für die Datei."
    
    # Datei erstellen
    if create_file(filename, content):
        # Dateigröße ermitteln
        size = get_file_size(filename)
        if size is not None:
            print(f"Dateigröße: {size} Bytes")
        
        # Dateiinhalt ausgeben
        file_content = read_file_content(filename)
        if file_content is not None:
            print("\nDateiinhalt:")
            print(file_content)

if __name__ == "__main__":
    main()
