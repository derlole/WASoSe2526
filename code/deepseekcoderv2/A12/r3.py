import csv

def sum_column(csv_file_path, column_name):
    total_sum = 0
    
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if column_name in row:
                try:
                    value = float(row[column_name])
                    total_sum += value
                except ValueError:
                    # Wenn der Wert nicht konvertiert werden kann, ignorieren wir ihn
                    pass
    
    return total_sum

# Beispielaufruf
csv_file_path = 'example.csv'
column_name = 'wert'
result = sum_column(csv_file_path, column_name)
print(f"Die Summe aller Werte in der Spalte '{column_name}' ist: {result}")