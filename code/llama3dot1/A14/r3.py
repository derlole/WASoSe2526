import os

def erstelle_datei(dateiname, inhalt):
    """
    Erstelle eine neue Datei mit dem angegebenen Namen und Inhalt.
    
    :param dateiname: Name der zu erstellenden Datei
    :type dateiname: str
    :param inhalt: Inhalt der Datei
    :type inhalt: str
    :return: Keine Rückgabewerte, da die Datei direkt im Dateisystem erstellt wird.
    """
    try:
        # Erstelle eine neue Datei mit dem angegebenen Namen und Inhalt
        with open(dateiname, 'w', encoding='utf-8') as datei:
            datei.write(inhalt)
    
    except Exception as e:
        print(f"Fehler bei der Erstellung der Datei '{dateiname}': {str(e)}")
        raise

def get_dateigröße(dateiname):
    """
    Richte eine neue Datei aus und ermittle ihre Größe.
    
    :param dateiname: Name der zu erstellenden Datei
    :type dateiname: str
    :return: Die Größe der Datei in Bytes
    """
    try:
        # Erstelle eine leere Datei mit dem angegebenen Namen und ermittle ihre Größe
        with open(dateiname, 'w', encoding='utf-8'):
            pass
        
        # Ermittle die Größe der Datei
        dateigröße = os.path.getsize(dateiname)
        
        return dateigröße
    
    except Exception as e:
        print(f"Fehler bei der Ermittlung der Dateigröße von '{dateiname}': {str(e)}")
        raise

def ausgabe_datei_inhalt(dateiname):
    """
    Lies den Inhalt einer bestehenden Datei und gib ihn zurück.
    
    :param dateiname: Name der zu lesenden Datei
    :type dateiname: str
    :return: Der Inhalt der Datei als String
    """
    try:
        # Öffne die Datei in Textmodus und liest ihren Inhalt
        with open(dateiname, 'r', encoding='utf-8') as datei:
            inhalt = datei.read()
        
        return inhalt
    
    except Exception as e:
        print(f"Fehler bei der Lesung des Inhalts von '{dateiname}': {str(e)}")
        raise

# Beispiel-Aufruf
if __name__ == "__main__":
    dateiname = "beispiel.txt"
    inhalt = "Dies ist ein Testinhalt."
    
    # Erstelle die Datei und gib ihre Größe aus
    erstelle_datei(dateiname, inhalt)
    dateigröße = get_dateigröße(dateiname)
    print(f"Größe der Datei '{dateiname}': {dateigröße} Bytes")
    
    # Lies den Inhalt der Datei und gib ihn aus
    inhalt = ausgabe_datei_inhalt(dateiname)
    print("Inhalt der Datei:")
    print(inhalt)