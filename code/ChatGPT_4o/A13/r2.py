import difflib

def compare_files(file1_path: str, file2_path: str):
    """
    Vergleicht zwei Dateien und gibt alle unterschiedlichen Zeilen zurück.
    
    Args:
        file1_path (str): Pfad zur ersten Datei.
        file2_path (str): Pfad zur zweiten Datei.
    
    Returns:
        List[Tuple[int, str, str]]: Liste von Unterschieden in Form von
        (Zeilennummer, Zeile in Datei1, Zeile in Datei2)
    """
    differences = []

    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    # Myers-Diff über difflib.ndiff
    diff = list(difflib.ndiff(file1_lines, file2_lines))

    line_num_file1 = 0
    line_num_file2 = 0

    for d in diff:
        code = d[:2]
        line = d[2:].rstrip("\n")
        
        if code == "  ":  # gleiche Zeile
            line_num_file1 += 1
            line_num_file2 += 1
        elif code == "- ":  # Zeile nur in Datei1
            differences.append((line_num_file1 + 1, line, None))
            line_num_file1 += 1
        elif code == "+ ":  # Zeile nur in Datei2
            differences.append((line_num_file2 + 1, None, line))
            line_num_file2 += 1
        elif code == "? ":  # Hinweis auf kleine Änderungen, kann ignoriert werden
            continue

    return differences


# Beispielnutzung
if __name__ == "__main__":
    file1 = "datei1.txt"
    file2 = "datei2.txt"
    
    diffs = compare_files(file1, file2)
    
    if not diffs:
        print("Die Dateien sind identisch.")
    else:
        print("Gefundene Unterschiede:")
        for line_num, line1, line2 in diffs:
            print(f"Zeile {line_num}:")
            print(f"  Datei1: {line1}")
            print(f"  Datei2: {line2}")
