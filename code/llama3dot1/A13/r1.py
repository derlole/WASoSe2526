import difflib

def diff_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    diff = matcher.find_longest_match(0, len(lines1), 0, len(lines2))

    # Führe die Diff-Algorithmen aus
    result = matcher.get_opcodes()

    # Filtere nur die Unterschiede heraus (A oder D)
    differenzen = [i for i in result if i[0] == 'A' or i[0] == 'D']

    return differenzen

# Beispielaufruf:
file1 = "datei1.txt"
file2 = "datei2.txt"

differenzen = diff_files(file1, file2)

print("Unterschiede:")
for differenz in differenzen:
    print(f"Liniennr.: {differenz[0]}, Änderung: {differenz[0]}-Linie ist {differenz[1]}")