import csv

def calculate_sum_of_column(file_path, column_name):
    total_sum = 0
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                value = float(row[column_name])
                total_sum += value
            except ValueError:
                # Skip rows where the column value is not a number
                continue

    return total_sum

# Example usage:
csv_file_path = 'data.csv'
column_to_sum = 'wert'
result = calculate_sum_of_column(csv_file_path, column_to_sum)
print(f"The sum of all values in the '{column_to_sum}' column is: {result}")