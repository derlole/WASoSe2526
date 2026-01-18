import csv

def sum_wert(csv_file):
    """
    Summiert alle Zahlen in der Spalte "wert" einer CSV-Datei.
    
    Args:
        csv_file (str): Der Pfad zur CSV-Datei
    
    Returns:
        float: Die Summe aller Zahlen in der Spalte "wert"
    """

    total = 0
    try:
        # Öffne die Datei zum Lesen, 'r' ist für lesen stehen
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            
            # Iteriere über jede Zeile in der CSV-Datei
            for row in reader:
                try:
                    # Versuche, den Wert von "wert" als float zu konvertieren und addiere ihn zum Gesamtwert
                    total += float(row['wert'])
                except (KeyError, ValueError):
                    # Wenn es keinen Eintrag für "wert" gibt oder der Eintrag nicht als Zahl umgewandelt werden kann, passiere weiter
                    pass
        
        return total
    
    except FileNotFoundError:
        print(f'Die Datei {csv_file} wurde nicht gefunden.')
    
    except Exception as e:
        print(f'Ein Fehler ist aufgetreten: {e}')

# Beispielaufruf für die Funktion
csv_file_path = 'pfad_zur_deine_csv_datei.csv'
summe = sum_wert(csv_file_path)
print(summe)