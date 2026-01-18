import csv

def sum_values_in_csv(file_path, column_name):
    total = 0

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                value = float(row[column_name])
                total += value
            except ValueError:
                # Ignore non-numeric values and continue with the next row
                continue

    return total

# Beispiel für die Verwendung der Funktion
file_path = 'data.csv'
column_name = 'wert'
result = sum_values_in_csv(file_path, column_name)
print(f"Die Summe aller Zahlen in der Spalte '{column_name}' ist: {result}")