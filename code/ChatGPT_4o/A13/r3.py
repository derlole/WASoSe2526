import difflib

def compare_files(file1_path, file2_path):
    """
    Vergleicht zwei Dateien und gibt alle unterschiedlichen Zeilen zurück.
    
    Args:
        file1_path (str): Pfad zur ersten Datei.
        file2_path (str): Pfad zur zweiten Datei.
        
    Returns:
        differences (list of dict): Jede Differenz mit Position und Zeileninhalt.
    """
    differences = []

    # Dateien zeilenweise öffnen
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Differenzen mithilfe von difflib (Myers-Diff) berechnen
    diff = difflib.ndiff(lines1, lines2)

    # Index für Zeilen in beiden Dateien
    index1 = index2 = 0

    for line in diff:
        code = line[:2]
        content = line[2:].rstrip('\n')

        if code == '  ':
            # Zeile gleich in beiden Dateien
            index1 += 1
            index2 += 1
        elif code == '- ':
            # Zeile nur in Datei1
            differences.append({
                'file': file1_path,
                'line_num': index1 + 1,
                'line_content': content,
                'type': 'removed'
            })
            index1 += 1
        elif code == '+ ':
            # Zeile nur in Datei2
            differences.append({
                'file': file2_path,
                'line_num': index2 + 1,
                'line_content': content,
                'type': 'added'
            })
            index2 += 1
        elif code == '? ':
            # Hinweis auf genaueren Unterschied innerhalb der Zeile (optional)
            pass

    return differences

# Beispielnutzung
if __name__ == "__main__":
    file1 = "datei1.txt"
    file2 = "datei2.txt"

    diffs = compare_files(file1, file2)
    for d in diffs:
        print(f"{d['type'].upper()} in {d['file']} Zeile {d['line_num']}: {d['line_content']}")
