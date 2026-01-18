import difflib

def diff_files(file1, file2):
    """
    Vergleicht zwei Dateien und findet alle unterschiedlichen Zeilen.

    Args:
        file1 (str): Pfad zur ersten Datei.
        file2 (str): Pfad zur zweiten Datei.

    Returns:
        dict: Ein Dictionary mit den unterschiedlichen Zeilen. Die Schlüssel sind die Zeilennummern der ersten Datei, die Werte sind Listen mit der Zeile aus der ersten und zweiten Datei.
    """
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    d = difflib.Differ(lines1, lines2)
    differences = {}

    for line in d.compare():
        if line.startswith('?'):
            continue  # Diese Zeile ist nur in einer der Dateien vorhanden
        elif line.startswith('+'):
            differences[line[1:].strip()] = (line[1:].strip(), None)  # Zeile aus zweiter Datei
        elif line.startswith('-'):
            differences[line[1:].strip()] = (None, line[1:].strip())  # Zeile aus erster Datei
        else:
            differences[line.strip()] = (line.strip(), line.strip())

    return differences

# Beispiel-Ausführung
file1 = 'datei1.txt'
file2 = 'datei2.txt'

differences = diff_files(file1, file2)

for line_num, diff in differences.items():
    print(f"Zeile {line_num}:")
    if diff[0] and diff[1]:
        print(f"Eine Zeile '{diff[0]}' und eine andere Zeile '{diff[1]}'")
    elif diff[0]:
        print(f"Hinzugefügt: '{diff[0]}'")
    elif diff[1]:
        print(f"Entfernt: '{diff[1]}'")