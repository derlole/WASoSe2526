import csv

def sum_column(file_path, column_name):
    total_sum = 0
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if column_name in row:
                try:
                    total_sum += float(row[column_name])
                except ValueError:
                    print(f"Warning: Skipping non-numeric value '{row[column_name]}' in column '{column_name}'.")
    
    return total_sum

# Beispielaufruf
file_path = 'example.csv'
column_name = 'wert'
result = sum_column(file_path, column_name)
print(f"The sum of the '{column_name}' column is: {result}")