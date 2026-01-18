import difflib

def compare_files(file1_path, file2_path):
    # Read the files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    # Use difflib to get the difference between two sequences of lines
    diff = difflib.ndiff(lines1, lines2)

    # Iterate through each character in the diff result
    for char in diff:
        if char != ' ':  # Skip equal lines
            print(char)

# Example usage
file1_path = 'path/to/first/file.txt'
file2_path = 'path/to/second/file.txt'
compare_files(file1_path, file2_path)