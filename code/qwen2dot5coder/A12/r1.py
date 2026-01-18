def sum_column_values(csv_file_path, column_name='wert'):
    total_sum = 0
    
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # Read the header line to get the index of the specified column
        header = file.readline().strip().split(',')
        
        if column_name not in header:
            raise ValueError(f"The column '{column_name}' does not exist in the CSV file.")
        
        column_index = header.index(column_name)
        
        for line in file:
            row = line.strip().split(',')
            
            # Check if the row has enough columns and is a valid number
            if len(row) > column_index and row[column_index].replace('.', '', 1).isdigit():
                total_sum += float(row[column_index])
    
    return total_sum

# Example usage:
csv_file_path = 'path_to_your_csv_file.csv'
result = sum_column_values(csv_file_path)
print(f"The sum of values in the '{column_name}' column is: {result}")