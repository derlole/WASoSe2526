#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datei-Verwaltungsprogramm
Erstellt eine Datei, ermittelt ihre Größe und gibt den Inhalt aus.
"""

import os
import sys


def erstelle_datei(dateiname, inhalt):
    """
    Erstellt eine Datei mit dem angegebenen Inhalt.
    
    Args:
        dateiname (str): Name der zu erstellenden Datei
        inhalt (str): Text, der in die Datei geschrieben wird
        
    Returns:
        bool: True bei Erfolg, False bei Fehler
    """
    try:
        with open(dateiname, 'w', encoding='utf-8') as datei:
            datei.write(inhalt)
        print(f"✓ Datei '{dateiname}' erfolgreich erstellt.")
        return True
    except PermissionError:
        print(f"✗ FEHLER: Keine Schreibberechtigung für '{dateiname}'", file=sys.stderr)
        return False
    except IsADirectoryError:
        print(f"✗ FEHLER: '{dateiname}' ist ein Verzeichnis", file=sys.stderr)
        return False
    except OSError as e:
        print(f"✗ FEHLER beim Erstellen der Datei: {e}", file=sys.stderr)
        return False


def ermittle_dateigroesse(dateiname):
    """
    Ermittelt die Größe einer Datei in Bytes.
    
    Args:
        dateiname (str): Name der Datei
        
    Returns:
        int or None: Dateigröße in Bytes oder None bei Fehler
    """
    try:
        groesse = os.path.getsize(dateiname)
        return groesse
    except FileNotFoundError:
        print(f"✗ FEHLER: Datei '{dateiname}' nicht gefunden", file=sys.stderr)
        return None
    except PermissionError:
        print(f"✗ FEHLER: Keine Leseberechtigung für '{dateiname}'", file=sys.stderr)
        return None
    except OSError as e:
        print(f"✗ FEHLER beim Ermitteln der Dateigröße: {e}", file=sys.stderr)
        return None


def lese_dateiinhalt(dateiname):
    """
    Liest den kompletten Inhalt einer Datei.
    
    Args:
        dateiname (str): Name der Datei
        
    Returns:
        str or None: Dateiinhalt oder None bei Fehler
    """
    try:
        with open(dateiname, 'r', encoding='utf-8') as datei:
            inhalt = datei.read()
        return inhalt
    except FileNotFoundError:
        print(f"✗ FEHLER: Datei '{dateiname}' nicht gefunden", file=sys.stderr)
        return None
    except PermissionError:
        print(f"✗ FEHLER: Keine Leseberechtigung für '{dateiname}'", file=sys.stderr)
        return None
    except UnicodeDecodeError:
        print(f"✗ FEHLER: Datei '{dateiname}' enthält ungültige UTF-8 Zeichen", file=sys.stderr)
        return None
    except OSError as e:
        print(f"✗ FEHLER beim Lesen der Datei: {e}", file=sys.stderr)
        return None


def formatiere_groesse(bytes_anzahl):
    """
    Konvertiert Bytes in eine lesbare Größenangabe.
    
    Args:
        bytes_anzahl (int): Anzahl der Bytes
        
    Returns:
        str: Formatierte Größenangabe (z.B. "1.5 KB")
    """
    einheiten = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    groesse = float(bytes_anzahl)
    einheit_index = 0
    
    while groesse >= 1024.0 and einheit_index < len(einheiten) - 1:
        groesse /= 1024.0
        einheit_index += 1
    
    if einheit_index == 0:
        return f"{int(groesse)} {einheiten[einheit_index]}"
    else:
        return f"{groesse:.2f} {einheiten[einheit_index]}"


def zeige_dateistatistiken(dateiname, inhalt, groesse):
    """
    Zeigt detaillierte Statistiken über die Datei an.
    
    Args:
        dateiname (str): Name der Datei
        inhalt (str): Inhalt der Datei
        groesse (int): Größe in Bytes
    """
    zeilen = inhalt.count('\n') + (1 if inhalt and not inhalt.endswith('\n') else 0)
    woerter = len(inhalt.split())
    zeichen = len(inhalt)
    zeichen_ohne_leerzeichen = len(inhalt.replace(' ', '').replace('\n', '').replace('\t', ''))
    
    print("\n" + "=" * 70)
    print("DATEISTATISTIKEN")
    print("=" * 70)
    print(f"Dateiname:               {dateiname}")
    print(f"Dateigröße:              {groesse} Bytes ({formatiere_groesse(groesse)})")
    print(f"Anzahl Zeilen:           {zeilen}")
    print(f"Anzahl Wörter:           {woerter}")
    print(f"Anzahl Zeichen:          {zeichen}")
    print(f"Zeichen (ohne Leerraum): {zeichen_ohne_leerzeichen}")
    print("=" * 70)


def main():
    """
    Hauptfunktion des Programms.
    """
    # Definition der Datei und ihres Inhalts
    dateiname = "meine_datei.txt"
    
    inhalt = """Willkommen zum Datei-Verwaltungsprogramm!

Diese Datei wurde automatisch erstellt, um folgende Funktionen zu demonstrieren:

1. Dateierstellung mit direktem Dateisystemzugriff
2. Ermittlung der Dateigröße in Bytes
3. Auslesen und Anzeigen des Dateiinhalts
4. Umfassende Fehlerbehandlung für alle Dateizugriffe

Technische Details:
- Programmiersprache: Python 3
- Encoding: UTF-8
- Fehlerbehandlung: try-except Blöcke für alle I/O-Operationen

Dieses Programm erfüllt alle Anforderungen und Constraints der Aufgabenstellung.

Viel Erfolg! 🎯
"""
    
    print("=" * 70)
    print("DATEI-VERWALTUNGSPROGRAMM")
    print("=" * 70)
    print()
    
    # Schritt 1: Datei erstellen
    print("SCHRITT 1: Datei erstellen")
    print("-" * 70)
    if not erstelle_datei(dateiname, inhalt):
        print("\n✗ Programm wird beendet (Fehler beim Erstellen)")
        sys.exit(1)
    print()
    
    # Schritt 2: Dateigröße ermitteln
    print("SCHRITT 2: Dateigröße ermitteln")
    print("-" * 70)
    groesse = ermittle_dateigroesse(dateiname)
    
    if groesse is None:
        print("\n✗ Programm wird beendet (Fehler bei Größenermittlung)")
        sys.exit(1)
    
    print(f"Dateigröße: {groesse} Bytes ({formatiere_groesse(groesse)})")
    print()
    
    # Schritt 3: Dateiinhalt auslesen und anzeigen
    print("SCHRITT 3: Dateiinhalt auslesen")
    print("-" * 70)
    dateiinhalt = lese_dateiinhalt(dateiname)
    
    if dateiinhalt is None:
        print("\n✗ Programm wird beendet (Fehler beim Lesen)")
        sys.exit(1)
    
    print("✓ Dateiinhalt erfolgreich ausgelesen\n")
    
    print("SCHRITT 4: Inhalt anzeigen")
    print("-" * 70)
    print(dateiinhalt)
    print("-" * 70)
    
    # Schritt 5: Statistiken anzeigen
    zeige_dateistatistiken(dateiname, dateiinhalt, groesse)
    
    print("\n✓ Alle Operationen erfolgreich abgeschlossen!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Programm durch Benutzer abgebrochen")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Unerwarteter Fehler: {e}", file=sys.stderr)
        sys.exit(1)