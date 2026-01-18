import csv

def summe_spalte_wert(csv_datei_pfad: str) -> float:
    """
    Liest eine CSV-Datei zeilenweise ein und summiert alle numerischen Werte
    in der Spalte 'wert'.

    Args:
        csv_datei_pfad (str): Pfad zur CSV-Datei

    Returns:
        float: Summe aller Werte in der Spalte 'wert'
    """
    gesamt_summe = 0.0

    with open(csv_datei_pfad, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        if 'wert' not in reader.fieldnames:
            raise ValueError("Die CSV-Datei enthält keine Spalte 'wert'.")
        
        for zeile in reader:
            wert_str = zeile.get('wert', '').strip()
            if wert_str:  # Nur wenn nicht leer
                try:
                    wert = float(wert_str)
                    gesamt_summe += wert
                except ValueError:
                    # Nicht-numerische Werte werden ignoriert
                    pass

    return gesamt_summe


# Beispiel für die Nutzung:
if __name__ == "__main__":
    datei = "daten.csv"  # Pfad zu deiner CSV-Datei
    ergebnis = summe_spalte_wert(datei)
    print(f"Summe der Spalte 'wert': {ergebnis}")
