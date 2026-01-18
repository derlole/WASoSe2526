#!/usr/bin/env python3
"""
CSV-Verarbeitung: Summiert alle numerischen Werte in der Spalte "wert"
Effizient für große Dateien durch Stream-Processing
"""

import csv
from typing import Union


def summe_wert_spalte(csv_datei: str, spaltenname: str = "wert") -> float:
    """
    Verarbeitet eine CSV-Datei und berechnet die Summe aller Zahlen in der
    spezifizierten Spalte.
    
    Args:
        csv_datei: Pfad zur CSV-Datei
        spaltenname: Name der zu summierenden Spalte (Standard: "wert")
    
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
        with open(csv_datei, 'r', encoding='utf-8') as datei:
            # CSV-Reader mit automatischer Dialekt-Erkennung
            csv_reader = csv.DictReader(datei)
            
            # Prüfe ob Spalte existiert
            if spaltenname not in csv_reader.fieldnames:
                verfuegbare = ', '.join(csv_reader.fieldnames)
                raise ValueError(
                    f"Spalte '{spaltenname}' nicht gefunden. "
                    f"Verfügbare Spalten: {verfuegbare}"
                )
            
            # Verarbeite Zeilen einzeln (Stream-Processing für große Dateien)
            for zeile in csv_reader:
                zeilen_verarbeitet += 1
                wert_str = zeile[spaltenname].strip()
                
                # Überspringe leere Werte
                if not wert_str:
                    continue
                
                # Versuche Wert zu konvertieren
                try:
                    # Unterstützt Komma und Punkt als Dezimaltrennzeichen
                    wert_str = wert_str.replace(',', '.')
                    wert = float(wert_str)
                    summe += wert
                except ValueError:
                    fehlerhafte_werte += 1
                    print(f"Warnung: Konnte Wert '{zeile[spaltenname]}' "
                          f"in Zeile {zeilen_verarbeitet} nicht konvertieren")
    
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV-Datei '{csv_datei}' nicht gefunden")
    
    print(f"\nVerarbeitung abgeschlossen:")
    print(f"  - Zeilen verarbeitet: {zeilen_verarbeitet}")
    print(f"  - Fehlerhafte Werte: {fehlerhafte_werte}")
    print(f"  - Summe: {summe}")
    
    return summe


def summe_wert_spalte_robust(
    csv_datei: str,
    spaltenname: str = "wert",
    delimiter: str = None,
    skip_errors: bool = True
) -> dict:
    """
    Erweiterte Version mit mehr Konfigurationsoptionen und detaillierten Stats.
    
    Args:
        csv_datei: Pfad zur CSV-Datei
        spaltenname: Name der zu summierenden Spalte
        delimiter: CSV-Trennzeichen (None = automatisch erkennen)
        skip_errors: True = Fehler überspringen, False = Exception werfen
    
    Returns:
        Dictionary mit Summe und Statistiken
    """
    summe = 0.0
    zeilen_gesamt = 0
    werte_summiert = 0
    fehler = []
    
    with open(csv_datei, 'r', encoding='utf-8') as datei:
        # Delimiter automatisch erkennen falls nicht angegeben
        if delimiter is None:
            sample = datei.read(1024)
            datei.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
        
        csv_reader = csv.DictReader(datei, delimiter=delimiter)
        
        if spaltenname not in csv_reader.fieldnames:
            raise ValueError(
                f"Spalte '{spaltenname}' nicht gefunden. "
                f"Verfügbar: {', '.join(csv_reader.fieldnames)}"
            )
        
        for idx, zeile in enumerate(csv_reader, start=2):  # Start bei 2 (Header = 1)
            zeilen_gesamt += 1
            wert_str = zeile[spaltenname].strip()
            
            if not wert_str:
                continue
            
            try:
                wert_str = wert_str.replace(',', '.')
                wert = float(wert_str)
                summe += wert
                werte_summiert += 1
            except ValueError as e:
                fehler.append({
                    'zeile': idx,
                    'wert': zeile[spaltenname],
                    'fehler': str(e)
                })
                if not skip_errors:
                    raise ValueError(
                        f"Ungültiger Wert in Zeile {idx}: '{zeile[spaltenname]}'"
                    )
    
    return {
        'summe': summe,
        'zeilen_gesamt': zeilen_gesamt,
        'werte_summiert': werte_summiert,
        'fehler_anzahl': len(fehler),
        'fehler': fehler,
        'durchschnitt': summe / werte_summiert if werte_summiert > 0 else 0
    }


# Beispiel-Verwendung und Tests
if __name__ == "__main__":
    import sys
    
    # Erstelle Test-CSV falls keine Datei angegeben
    if len(sys.argv) < 2:
        print("Erstelle Beispiel-CSV zum Testen...\n")
        
        test_datei = "test_daten.csv"
        with open(test_datei, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'wert', 'kategorie'])
            writer.writerow(['Artikel A', '10.5', 'Typ1'])
            writer.writerow(['Artikel B', '25,75', 'Typ2'])  # Komma-Format
            writer.writerow(['Artikel C', '15', 'Typ1'])
            writer.writerow(['Artikel D', '30.25', 'Typ3'])
            writer.writerow(['Artikel E', '', 'Typ1'])  # Leerer Wert
            writer.writerow(['Artikel F', '12.5', 'Typ2'])
        
        print("=== Einfache Variante ===")
        ergebnis = summe_wert_spalte(test_datei)
        print(f"\nGesamtsumme: {ergebnis}\n")
        
        print("=== Erweiterte Variante mit Statistiken ===")
        stats = summe_wert_spalte_robust(test_datei)
        print(f"Summe: {stats['summe']}")
        print(f"Durchschnitt: {stats['durchschnitt']:.2f}")
        print(f"Werte summiert: {stats['werte_summiert']} von {stats['zeilen_gesamt']}")
        
    else:
        # Verarbeite angegebene Datei
        datei = sys.argv[1]
        spalte = sys.argv[2] if len(sys.argv) > 2 else "wert"
        
        try:
            ergebnis = summe_wert_spalte(datei, spalte)
            print(f"\n✓ Gesamtsumme der Spalte '{spalte}': {ergebnis}")
        except Exception as e:
            print(f"✗ Fehler: {e}")
            sys.exit(1)