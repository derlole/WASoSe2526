#!/usr/bin/env python3
"""
CSV-Processor: Berechnet die Summe aller numerischen Werte in der Spalte 'wert'
Effiziente Stream-Verarbeitung für große Dateien ohne externe Frameworks
"""

import csv
import sys
from typing import Union, Optional


def sum_wert_spalte(csv_datei: str, 
                    spaltenname: str = "wert", 
                    delimiter: str = ",", 
                    encoding: str = "utf-8") -> float:
    """
    Verarbeitet eine CSV-Datei und summiert alle numerischen Werte in der angegebenen Spalte.
    
    Args:
        csv_datei: Pfad zur CSV-Datei
        spaltenname: Name der zu summierenden Spalte (Standard: "wert")
        delimiter: CSV-Trennzeichen (Standard: ",")
        encoding: Datei-Encoding (Standard: "utf-8")
    
    Returns:
        Summe aller numerischen Werte in der Spalte
    
    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert
        ValueError: Wenn die Spalte nicht gefunden wird
    """
    summe = 0.0
    zeilen_verarbeitet = 0
    fehlerhafte_werte = 0
    
    try:
        with open(csv_datei, 'r', encoding=encoding, newline='') as datei:
            # DictReader für benannte Spaltenzugriffe
            reader = csv.DictReader(datei, delimiter=delimiter)
            
            # Prüfe ob Spalte existiert
            if spaltenname not in reader.fieldnames:
                verfuegbare = ", ".join(reader.fieldnames)
                raise ValueError(
                    f"Spalte '{spaltenname}' nicht gefunden. "
                    f"Verfügbare Spalten: {verfuegbare}"
                )
            
            # Stream-Verarbeitung: Eine Zeile nach der anderen (speichereffizient)
            for zeile_nr, zeile in enumerate(reader, start=2):
                wert_str = zeile[spaltenname]
                
                # Überspringe leere Werte
                if not wert_str or wert_str.strip() == '':
                    continue
                
                try:
                    # Parse numerischen Wert
                    # Unterstützt deutsche Zahlenformate (Komma -> Punkt)
                    wert_str = wert_str.strip().replace(',', '.')
                    wert = float(wert_str)
                    summe += wert
                    zeilen_verarbeitet += 1
                    
                except ValueError:
                    fehlerhafte_werte += 1
                    print(f"Warnung: Nicht-numerischer Wert in Zeile {zeile_nr}: '{wert_str}'", 
                          file=sys.stderr)
    
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV-Datei nicht gefunden: {csv_datei}")
    
    except UnicodeDecodeError:
        raise ValueError(
            f"Encoding-Fehler bei '{csv_datei}'. "
            f"Versuchen Sie ein anderes Encoding (z.B. 'latin-1', 'iso-8859-1')"
        )
    
    # Ausgabe Statistik
    print(f"Verarbeitete Zeilen: {zeilen_verarbeitet}")
    if fehlerhafte_werte > 0:
        print(f"Fehlerhafte Werte übersprungen: {fehlerhafte_werte}")
    
    return summe


def main():
    """Hauptfunktion für Kommandozeilen-Verwendung"""
    if len(sys.argv) < 2:
        print("Verwendung: python csv_processor.py <csv_datei> [spaltenname] [delimiter]")
        print("\nBeispiele:")
        print("  python csv_processor.py daten.csv")
        print("  python csv_processor.py daten.csv betrag")
        print("  python csv_processor.py daten.csv wert ';'")
        sys.exit(1)
    
    csv_datei = sys.argv[1]
    spaltenname = sys.argv[2] if len(sys.argv) > 2 else "wert"
    delimiter = sys.argv[3] if len(sys.argv) > 3 else ","
    
    try:
        print(f"Verarbeite '{csv_datei}'...")
        summe = sum_wert_spalte(csv_datei, spaltenname, delimiter)
        print(f"\n✓ Summe der Spalte '{spaltenname}': {summe}")
        
    except Exception as e:
        print(f"\n✗ Fehler: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()