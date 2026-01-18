import csv

def sum_column(filename, column_name):
    total = 0
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Versuche den Wert in der Spalte zu konvertieren und zur Summe hinzuzufügen
                total += float(row[column_name])
            except (ValueError, KeyError):
                # Ignoriere Zeilen mit Fehlern (z.B. Nicht-Zahlen oder fehlende Spalten)
                pass
    return total

# Beispiel: Verwende die Funktion mit einer Datei namens "data.csv"
filename = 'data.csv'
column_name = 'wert'
result = sum_column(filename, column_name)
print(f"Die Summe aller Zahlen in der Spalte '{column_name}' ist: {result}")