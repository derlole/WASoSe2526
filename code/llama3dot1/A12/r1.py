import csv

def sum_werte(csv_file):
    """
    Berechne die Summe aller Zahlen in der Spalte "wert" einer CSV-Datei.
    
    Args:
        csv_file (str): Der Pfad zur CSV-Datei
    
    Returns:
        float: Die Summe aller Zahlen in der Spalte "wert"
    """

    total = 0
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Überprüfe, ob die Spalte "wert" existiert und ist numerisch
        has_wert_column = False
        for row in reader:
            if 'wert' in row and row['wert'].replace('.', '', 1).isdigit():
                total += float(row['wert'])
                has_wert_column = True
        
        # Wenn die Spalte "wert" nicht existiert, oder wenn alle Werte nicht numerisch sind
        if not has_wert_column:
            raise ValueError("Die CSV-Datei enthält keine 'wert'-Spalte, oder alle Werte in dieser Spalte sind nicht numerisch.")
    
    return total

# Beispielaufruf der Funktion
csv_file = 'path_to_your_csv_file.csv'  # Ersetzen durch Ihren Dateipfad
result = sum_werte(csv_file)
print(f'Summe aller Zahlen in der "wert"-Spalte: {result}')