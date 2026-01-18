import csv

def summe_wert(csv_datei: str) -> float:
    """
    Berechnet die Summe aller Zahlen in der Spalte 'wert' einer CSV-Datei.

    :param csv_datei: Pfad zur CSV-Datei
    :return: Summe der Werte in der Spalte 'wert'
    """
    summe = 0.0

    with open(csv_datei, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        if 'wert' not in reader.fieldnames:
            raise ValueError("Die CSV-Datei enthält keine Spalte 'wert'.")

        for zeile in reader:
            try:
                wert = float(zeile['wert'])
                summe += wert
            except ValueError:
                # Zeile ignorieren, wenn Wert nicht konvertierbar ist
                pass

    return summe

# Beispielaufruf
if __name__ == "__main__":
    dateipfad = "daten.csv"
    ergebnis = summe_wert(dateipfad)
    print(f"Die Summe der 'wert'-Spalte beträgt: {ergebnis}")
