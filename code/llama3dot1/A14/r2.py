import os

def erstelle_datei(inhalt):
    """
    Erstellt eine neue Datei mit dem angegebenen Inhalt.
    
    Args:
        inhalt (str): Der zu schreibende Inhalt der Datei.
        
    Returns:
        str: Die Dateipfade, unter denen die Datei gespeichert wurde.
    """
    # Ermitteln eines freien Orts zum Speichern der Datei
    dateiname = "erstelle_datei.txt"
    
    try:
        # Versuch, eine neue Datei zu erstellen
        with open(dateiname, 'w') as file:
            # Schreiben des Inhalts in die Datei
            file.write(inhalt)
            
        return dateiname
    
    except Exception as e:
        print(f"Fehler bei der Erstellung der Datei: {str(e)}")
        return None

def les_datei(dateipfad):
    """
    Liest den Inhalt einer Datei aus und gibt ihn zurück.
    
    Args:
        dateipfad (str): Der Pfad zur Datei, die gelesen werden soll.
        
    Returns:
        str: Der Inhalt der Datei oder None falls ein Fehler auftritt.
    """
    try:
        # Versuch, den Inhalt der Datei zu lesen
        with open(dateipfad, 'r') as file:
            return file.read()
    
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {str(e)}")
        return None

def berechne_dateigröße(dateipfad):
    """
    Berechnet die Größe einer Datei in Bytes.
    
    Args:
        dateipfad (str): Der Pfad zur Datei, für deren Größe abgefragt werden soll.
        
    Returns:
        int: Die Dateigröße in Bytes oder -1 falls ein Fehler auftritt.
    """
    try:
        # Versuch, die Dateigröße zu ermitteln
        return os.path.getsize(dateipfad)
    
    except Exception as e:
        print(f"Fehler beim Ermitteln der Dateigröße: {str(e)}")
        return -1

# Beispielverwendung des Programms
if __name__ == "__main__":
    # Erstellen einer neuen Datei mit Inhalt
    dateipfad = erstelle_datei("Dies ist ein Test in einer neu erstellten Datei.")
    
    if dateipfad:
        print(f"Datei '{dateipfad}' erfolgreich erstellt.")
        
        # Auslesen des Inhalts der Datei und Ausgabe seiner Größe
        content = les_datei(dateipfad)
        size = berechne_dateigröße(dateipfad)
        
        if content and size != -1:
            print(f"Inhalt der Datei: {content}")
            print(f"Dateigröße: {size} Byte")
        else:
            print("Fehler beim Auslesen des Inhalts oder Ermitteln der Größe.")
            
    else:
        print("Fehler beim Erstellen der Datei.")