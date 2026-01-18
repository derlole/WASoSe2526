import csv

def sum_values(csv_file_path):
    total = 0

    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Versuche den Wert als Zahl zu konvertieren und zur Summe hinzuzufügen
                value = float(row['wert'])
                total += value
            except (ValueError, KeyError):
                # Ignoriere Zeilen, die nicht die Spalte "wert" enthalten oder den Wert nicht als Zahl konvertieren können
                continue

    return total

# Beispiel: Verwendung der Funktion
csv_file_path = 'path/to/your/csvfile.csv'
result = sum_values(csv_file_path)
print("Summe aller Zahlen in der Spalte 'wert':", result)