import difflib

def compare_files(file1_path, file2_path):
    # Read the content of the first file
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file1_lines = file1.readlines()

    # Read the content of the second file
    with open(file2_path, 'r', encoding='utf-8') as file2:
        file2_lines = file2.readlines()

    # Use difflib to find differences between the two files
    diff = difflib.unified_diff(
        file1_lines,
        file2_lines,
        fromfile=file1_path,
        tofile=file2_path,
        lineterm='',
        n=0
    )

    # Collect and print the differences
    differences = []
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            differences.append(line)

    return differences

# Example usage
file1_path = 'path/to/file1.txt'
file2_path = 'path/to/file2.txt'

differences = compare_files(file1_path, file2_path)
for diff in differences:
    print(diff.strip())