import difflib

def compare_files(file1_path, file2_path):
    """
    Vergleicht zwei Dateien und gibt alle unterschiedlichen Zeilen mit Position zurück.
    
    :param file1_path: Pfad zur ersten Datei
    :param file2_path: Pfad zur zweiten Datei
    :return: Liste von Unterschieden in Form von dicts:
             [{"line_num_file1": int, "line_file1": str, 
               "line_num_file2": int, "line_file2": str}]
    """
    differences = []

    # Dateien zeilenweise einlesen (speicherfreundlich auch bei großen Dateien)
    with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1:
        lines1 = f1.readlines()
    with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
        lines2 = f2.readlines()
    
    # Differenz-Generator von difflib (Myers-Algorithmus)
    diff = difflib.ndiff(lines1, lines2)
    
    line_num1 = 0
    line_num2 = 0

    for line in diff:
        code = line[:2]
        content = line[2:]
        if code == '  ':  # Keine Änderung
            line_num1 += 1
            line_num2 += 1
        elif code == '- ':  # Zeile nur in Datei1
            differences.append({
                "line_num_file1": line_num1 + 1,
                "line_file1": content.rstrip('\n'),
                "line_num_file2": None,
                "line_file2": None
            })
            line_num1 += 1
        elif code == '+ ':  # Zeile nur in Datei2
            differences.append({
                "line_num_file1": None,
                "line_file1": None,
                "line_num_file2": line_num2 + 1,
                "line_file2": content.rstrip('\n')
            })
            line_num2 += 1
        elif code == '? ':  # Zeilenhinweis von difflib, kann ignoriert werden
            continue

    return differences

# Beispielnutzung
if __name__ == "__main__":
    file1 = "datei1.txt"
    file2 = "datei2.txt"
    diffs = compare_files(file1, file2)
    
    for d in diffs:
        print(d)
