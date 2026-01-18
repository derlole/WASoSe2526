#!/usr/bin/env python3
"""
CSV Processor - Summiert numerische Werte aus einer CSV-Datei
Effiziente Verarbeitung auch für große Dateien ohne externe Frameworks
"""

import csv
import sys
from typing import Union
from pathlib import Path


def parse_numeric_value(value: str) -> float:
    """
    Konvertiert einen String-Wert in eine Zahl.
    Unterstützt verschiedene Formate wie Komma-Dezimaltrennzeichen.
    
    Args:
        value: String-Wert zum Parsen
        
    Returns:
        Numerischer Wert als float
        
    Raises:
        ValueError: Wenn der Wert nicht in eine Zahl konvertiert werden kann
    """
    # Entferne Whitespace
    value = value.strip()
    
    # Ersetze deutsches Dezimaltrennzeichen (Komma) durch Punkt
    value = value.replace(',', '.')
    
    # Entferne Tausendertrennzeichen (Punkt oder Leerzeichen)
    value = value.replace(' ', '')
    
    # Wenn ein Punkt als Tausendertrenner verwendet wurde (z.B. 1.000.000,50)
    # würde bereits das Komma ersetzt sein, also müssen wir prüfen
    # ob mehrere Punkte vorhanden sind
    if value.count('.') > 1:
        # Entferne alle Punkte außer dem letzten (Dezimaltrennzeichen)
        parts = value.rsplit('.', 1)
        value = parts[0].replace('.', '') + '.' + parts[1]
    
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Kann '{value}' nicht in eine Zahl konvertieren")


def sum_csv_column(
    filepath: Union[str, Path],
    column_name: str = "wert",
    encoding: str = "utf-8",
    delimiter: str = ",",
    skip_errors: bool = False
) -> dict:
    """
    Verarbeitet eine CSV-Datei und berechnet die Summe aller Zahlen in der angegebenen Spalte.
    
    Args:
        filepath: Pfad zur CSV-Datei
        column_name: Name der Spalte, deren Werte summiert werden sollen
        encoding: Zeichenkodierung der Datei (default: utf-8)
        delimiter: CSV-Trennzeichen (default: ,)
        skip_errors: Wenn True, werden ungültige Werte übersprungen (default: False)
        
    Returns:
        Dictionary mit Ergebnissen:
        - 'sum': Gesamtsumme
        - 'count': Anzahl der verarbeiteten Werte
        - 'errors': Anzahl der Fehler (wenn skip_errors=True)
        - 'rows_processed': Gesamtanzahl der Zeilen
        
    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert
        ValueError: Wenn die Spalte nicht gefunden wird oder Werte ungültig sind
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")
    
    total_sum = 0.0
    value_count = 0
    error_count = 0
    rows_processed = 0
    column_found = False
    
    # Verarbeite die CSV-Datei zeilenweise für Speichereffizienz
    with open(filepath, 'r', encoding=encoding, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        
        # Prüfe ob die Spalte existiert
        if reader.fieldnames and column_name not in reader.fieldnames:
            available_columns = ', '.join(reader.fieldnames)
            raise ValueError(
                f"Spalte '{column_name}' nicht gefunden. "
                f"Verfügbare Spalten: {available_columns}"
            )
        
        column_found = True
        
        # Verarbeite jede Zeile
        for row_num, row in enumerate(reader, start=2):  # start=2 wegen Header
            rows_processed += 1
            
            # Hole den Wert aus der Spalte
            value_str = row.get(column_name, '').strip()
            
            # Überspringe leere Werte
            if not value_str:
                if skip_errors:
                    error_count += 1
                    continue
                else:
                    raise ValueError(
                        f"Leerer Wert in Zeile {row_num}, Spalte '{column_name}'"
                    )
            
            # Parse und summiere den Wert
            try:
                numeric_value = parse_numeric_value(value_str)
                total_sum += numeric_value
                value_count += 1
            except ValueError as e:
                if skip_errors:
                    error_count += 1
                    print(
                        f"Warnung: Zeile {row_num} übersprungen - {e}",
                        file=sys.stderr
                    )
                else:
                    raise ValueError(
                        f"Fehler in Zeile {row_num}, Spalte '{column_name}': {e}"
                    )
    
    if not column_found:
        raise ValueError("CSV-Datei enthält keine Header-Zeile")
    
    return {
        'sum': total_sum,
        'count': value_count,
        'errors': error_count,
        'rows_processed': rows_processed
    }


def main():
    """Kommandozeilen-Interface für das Skript"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Summiert numerische Werte aus einer CSV-Spalte'
    )
    parser.add_argument(
        'filepath',
        help='Pfad zur CSV-Datei'
    )
    parser.add_argument(
        '-c', '--column',
        default='wert',
        help='Name der zu summierenden Spalte (default: wert)'
    )
    parser.add_argument(
        '-d', '--delimiter',
        default=',',
        help='CSV-Trennzeichen (default: ,)'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf-8',
        help='Zeichenkodierung (default: utf-8)'
    )
    parser.add_argument(
        '-s', '--skip-errors',
        action='store_true',
        help='Überspringe ungültige Werte statt abzubrechen'
    )
    
    args = parser.parse_args()
    
    try:
        result = sum_csv_column(
            filepath=args.filepath,
            column_name=args.column,
            encoding=args.encoding,
            delimiter=args.delimiter,
            skip_errors=args.skip_errors
        )
        
        print(f"\n{'='*50}")
        print(f"Ergebnis für Spalte '{args.column}':")
        print(f"{'='*50}")
        print(f"Summe:              {result['sum']:,.2f}")
        print(f"Anzahl Werte:       {result['count']}")
        print(f"Zeilen verarbeitet: {result['rows_processed']}")
        
        if args.skip_errors and result['errors'] > 0:
            print(f"Fehler übersprungen: {result['errors']}")
        
        print(f"{'='*50}\n")
        
    except Exception as e:
        print(f"Fehler: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()