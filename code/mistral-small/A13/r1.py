import difflib

def find_differences(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    diff = difflib.unified_diff(lines1, lines2, lineterm='')

    differences = []
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            # Extracting the position and line number from unified diff format
            position = int(line[4:-1]) + 1  # Unified diff uses 0-based index for context lines
            differences.append((position, line))

    return differences

# Example usage:
file1_path = 'path/to/your/first/file.txt'
file2_path = 'path/to/your/second/file.txt'
differences = find_differences(file1_path, file2_path)

for position, line in differences:
    print(f"Position {position}: {line}")