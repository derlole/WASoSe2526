import csv

def sum_column_values(csv_file_path, column_name):
    total_sum = 0
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                value = float(row[column_name])
                total_sum += value
            except (ValueError, KeyError):
                # Ignoriere Zeilen, die den gewünschten Spaltennamen nicht haben oder das Konvertieren fehlschlägt
                continue

    return total_sum

# Beispielaufruf:
csv_file_path = 'your_file.csv'  # Ersetze dies durch den Pfad zu deiner CSV-Datei
column_name = 'wert'  # Ersetze dies durch den Namen der gewünschten Spalte
result = sum_column_values(csv_file_path, column_name)
print(f"Die Summe aller Werte in der Spalte '{column_name}' beträgt: {result}")