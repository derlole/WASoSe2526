#!/usr/bin/env python3
"""
Programm zur Dateierstellung mit Größen- und Inhaltsanzeige
"""

import os
import sys


def datei_erstellen(dateiname, inhalt):
    """
    Erstellt eine Datei mit dem angegebenen Inhalt.
    
    Args:
        dateiname: Name der zu erstellenden Datei
        inhalt: Inhalt, der in die Datei geschrieben werden soll
    
    Returns:
        bool: True bei Erfolg, False bei Fehler
    """
    try:
        with open(dateiname, 'w', encoding='utf-8') as datei:
            datei.write(inhalt)
        print(f"✓ Datei '{dateiname}' erfolgreich erstellt.")
        return True
    except PermissionError:
        print(f"✗ Fehler: Keine Berechtigung zum Erstellen der Datei '{dateiname}'.", 
              file=sys.stderr)
        return False
    except OSError as e:
        print(f"✗ Fehler beim Erstellen der Datei '{dateiname}': {e}", 
              file=sys.stderr)
        return False


def dateigroesse_ermitteln(dateiname):
    """
    Ermittelt die Größe einer Datei in Bytes.
    
    Args:
        dateiname: Name der Datei
    
    Returns:
        int: Größe in Bytes oder None bei Fehler
    """
    try:
        groesse = os.path.getsize(dateiname)
        return groesse
    except FileNotFoundError:
        print(f"✗ Fehler: Datei '{dateiname}' nicht gefunden.", file=sys.stderr)
        return None
    except OSError as e:
        print(f"✗ Fehler beim Ermitteln der Dateigröße: {e}", file=sys.stderr)
        return None


def datei_lesen(dateiname):
    """
    Liest den Inhalt einer Datei.
    
    Args:
        dateiname: Name der zu lesenden Datei
    
    Returns:
        str: Dateiinhalt oder None bei Fehler
    """
    try:
        with open(dateiname, 'r', encoding='utf-8') as datei:
            inhalt = datei.read()
        return inhalt
    except FileNotFoundError:
        print(f"✗ Fehler: Datei '{dateiname}' nicht gefunden.", file=sys.stderr)
        return None
    except PermissionError:
        print(f"✗ Fehler: Keine Berechtigung zum Lesen der Datei '{dateiname}'.", 
              file=sys.stderr)
        return None
    except UnicodeDecodeError:
        print(f"✗ Fehler: Datei '{dateiname}' enthält ungültiges UTF-8.", 
              file=sys.stderr)
        return None
    except OSError as e:
        print(f"✗ Fehler beim Lesen der Datei '{dateiname}': {e}", file=sys.stderr)
        return None


def bytes_formatieren(bytes_anzahl):
    """
    Formatiert Bytes in eine lesbare Größenangabe.
    
    Args:
        bytes_anzahl: Anzahl der Bytes
    
    Returns:
        str: Formatierte Größenangabe
    """
    for einheit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_anzahl < 1024.0:
            return f"{bytes_anzahl:.2f} {einheit}"
        bytes_anzahl /= 1024.0
    return f"{bytes_anzahl:.2f} PB"


def main():
    """Hauptfunktion des Programms."""
    
    # Dateiname und Inhalt definieren
    dateiname = "beispiel_datei.txt"
    inhalt = """Dies ist eine Beispieldatei.
Sie enthält mehrere Zeilen Text.

Mit diesem Programm demonstrieren wir:
- Dateierstellung
- Größenermittlung
- Inhaltsanzeige

Erstellt am: 2026-01-18
"""
    
    print("=" * 60)
    print("Datei-Verwaltungsprogramm")
    print("=" * 60)
    print()
    
    # Schritt 1: Datei erstellen
    print("Schritt 1: Datei erstellen")
    print("-" * 60)
    if not datei_erstellen(dateiname, inhalt):
        return 1
    print()
    
    # Schritt 2: Dateigröße ermitteln
    print("Schritt 2: Dateigröße ermitteln")
    print("-" * 60)
    groesse = dateigroesse_ermitteln(dateiname)
    if groesse is None:
        return 1
    print(f"Dateigröße: {groesse} Bytes ({bytes_formatieren(groesse)})")
    print()
    
    # Schritt 3: Dateiinhalt lesen und anzeigen
    print("Schritt 3: Dateiinhalt anzeigen")
    print("-" * 60)
    inhalt_gelesen = datei_lesen(dateiname)
    if inhalt_gelesen is None:
        return 1
    
    print(f"Inhalt der Datei '{dateiname}':")
    print()
    print("┌" + "─" * 58 + "┐")
    for zeile in inhalt_gelesen.split('\n'):
        print(f"│ {zeile:<56} │")
    print("└" + "─" * 58 + "┘")
    print()
    
    # Zusätzliche Statistiken
    print("Statistiken:")
    print("-" * 60)
    zeilen_anzahl = len(inhalt_gelesen.split('\n'))
    zeichen_anzahl = len(inhalt_gelesen)
    woerter_anzahl = len(inhalt_gelesen.split())
    
    print(f"Anzahl der Zeilen:   {zeilen_anzahl}")
    print(f"Anzahl der Zeichen:  {zeichen_anzahl}")
    print(f"Anzahl der Wörter:   {woerter_anzahl}")
    print()
    
    print("=" * 60)
    print("Programm erfolgreich abgeschlossen!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())