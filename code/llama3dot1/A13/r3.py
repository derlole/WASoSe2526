import difflib

def diff_files(file1, file2):
    """
    Vergleicht zwei Dateien und findet alle unterschiedlichen Zeilen.

    Args:
        file1 (str): Dateiname der ersten Datei.
        file2 (str): Dateiname der zweiten Datei.

    Returns:
        Eine Liste von Tupeln, wobei jeder Tupel die Positionsdaten einer unterschiedlichen Zeile enthält.
            Der erste Element des Tupels ist eine Boolesche Variable, die `True` ergibt, wenn in der ersten Datei mehr Informationen
                vorhanden sind als in der zweiten. Das zweite Element ist eine Boolesche Variable, die `True` ergibt,
                wenn in der zweiten Datei mehr Informationen vorhanden sind als in der ersten.
            Der dritte Element des Tupels ist die Position der unterschiedlichen Zeile (von 0 bis einschließlich).
    """
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    differences = []
    for a, b in zip(lines1, lines2):
        if a.strip() != b.strip():
            diff_a = True
            diff_b = False
            diff_pos = lines1.index(a)
            if len(b) > len(a) or (len(a) == len(b) and b > a):
                diff_b = True
            differences.append((diff_a, diff_b, diff_pos))

    for pos in range(len(lines1)):
        if lines1[pos].strip() != '':
            found = False
            for difference in differences:
                if difference[2] < pos and not found:
                    found = True
                elif difference[2] == pos:
                    break
            else:
                diff_a = True
                diff_b = False
                differences.append((diff_a, diff_b, pos))

    return differences

# Beispiel:
file1 = 'datei1.txt'
file2 = 'datei2.txt'

differences = diff_files(file1, file2)
print(differences)

for difference in differences:
    if difference[0]:
        print(f'In {file1} enthält die Zeile um {difference[2]} Position mehr Informationen als in {file2}.')
    elif difference[1]:
        print(f'In {file2} enthält die Zeile um {difference[2]} Position mehr Informationen als in {file1}.')