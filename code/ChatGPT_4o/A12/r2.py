import csv

def sum_csv_column(file_path, column_name="wert"):
    """
    Berechnet die Summe aller Zahlen in der angegebenen Spalte einer CSV-Datei.

    Args:
        file_path (str): Pfad zur CSV-Datei
        column_name (str): Name der Spalte, deren Werte summiert werden sollen (default "wert")

    Returns:
        float: Summe der Werte in der Spalte
    """
    total = 0.0
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if column_name not in reader.fieldnames:
            raise ValueError(f"Spalte '{column_name}' existiert nicht in der CSV-Datei.")
        for row in reader:
            value = row.get(column_name, "").strip()
            if value:  # Ignoriere leere Felder
                try:
                    total += float(value)
                except ValueError:
                    # Optional: Warnung ausgeben, wenn Wert nicht konvertierbar ist
                    print(f"Warnung: Wert '{value}' in Zeile {reader.line_num} ist keine Zahl und wird ignoriert.")
    return total

# Beispielaufruf
if __name__ == "__main__":
    file_path = "daten.csv"  # Pfad zur CSV-Datei anpassen
    result = sum_csv_column(file_path)
    print(f"Summe der Spalte 'wert': {result}")
