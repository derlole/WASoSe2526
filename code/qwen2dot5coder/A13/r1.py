import difflib

def compare_files(file1_path, file2_path):
    # Read the contents of both files
    with open(file1_path, 'r', encoding='utf-8') as file1:
        lines1 = file1.readlines()
    
    with open(file2_path, 'r', encoding='utf-8') as file2:
        lines2 = file2.readlines()

    # Use difflib to find differences
    diff = difflib.unified_diff(lines1, lines2, fromfile=file1_path, tofile=file2_path, lineterm='')

    # Collect and print the differing lines with their positions
    for line in diff:
        if line.startswith('-'):
            # Line is removed (difference in file1)
            print(f"Removed: {line[1:]}", end='')
        elif line.startswith('+'):
            # Line is added (difference in file2)
            print(f"Added: {line[1:]}", end='')

# Example usage
compare_files('file1.txt', 'file2.txt')