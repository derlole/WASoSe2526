import csv

def sum_column(file_path, column_name):
    total_sum = 0
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            value = row.get(column_name)
            if value is not None and value.strip() != "":  # Ensure the value is numeric or can be converted to a number
                try:
                    total_sum += float(value)
                except ValueError:
                    print(f"Warning: Skipping non-numeric value '{value}' in row {reader.line_num}")
    
    return total_sum

# Example usage:
file_path = 'data.csv'  # Path to your CSV file
column_name = 'wert'  # Name of the column you want to sum
result = sum_column(file_path, column_name)
print(f"The sum of '{column_name}' in the CSV is: {result}")