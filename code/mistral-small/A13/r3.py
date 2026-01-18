import difflib

def find_file_differences(file1, file2):
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()

    with open(file2, 'r') as f2:
        lines2 = f2.readlines()

    diff = difflib.ndiff(lines1, lines2)

    differences = []
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            idx = int(line[2:].split(',')[0]) + 1
            differences.append((idx, line))

    return differences

# Example usage:
file1 = "file1.txt"
file2 = "file2.txt"
differences = find_file_differences(file1, file2)

for diff in differences:
    print(f"Difference at line {diff[0]}: {diff[1].strip()}")