#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programm zum Erstellen einer Datei und Anzeigen ihrer Größe und Inhalte
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
        True bei Erfolg, False bei Fehler
    """
    try:
        with open(dateiname, 'w', encoding='utf-8') as datei:
            datei.write(inhalt)
        print(f"✓ Datei '{dateiname}' erfolgreich erstellt.")
        return True
    except IOError as e:
        print(f"✗ Fehler beim Erstellen der Datei: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}", file=sys.stderr)
        return False


def dateigroesse_ermitteln(dateiname):
    """
    Ermittelt die Größe einer Datei in Bytes.
    
    Args:
        dateiname: Name der Datei
    
    Returns:
        Größe in Bytes oder None bei Fehler
    """
    try:
        groesse = os.path.getsize(dateiname)
        return groesse
    except FileNotFoundError:
        print(f"✗ Fehler: Datei '{dateiname}' nicht gefunden.", file=sys.stderr)
        return None
    except OSError as e:
        print(f"✗ Fehler beim Abrufen der Dateigröße: {e}", file=sys.stderr)
        return None


def dateiinhalt_lesen(dateiname):
    """
    Liest den Inhalt einer Datei.
    
    Args:
        dateiname: Name der Datei
    
    Returns:
        Inhalt der Datei oder None bei Fehler
    """
    try:
        with open(dateiname, 'r', encoding='utf-8') as datei:
            inhalt = datei.read()
        return inhalt
    except FileNotFoundError:
        print(f"✗ Fehler: Datei '{dateiname}' nicht gefunden.", file=sys.stderr)
        return None
    except IOError as e:
        print(f"✗ Fehler beim Lesen der Datei: {e}", file=sys.stderr)
        return None
    except UnicodeDecodeError as e:
        print(f"✗ Fehler beim Dekodieren der Datei: {e}", file=sys.stderr)
        return None


def groesse_formatieren(bytes_groesse):
    """
    Formatiert Bytes in eine lesbare Größenangabe.
    
    Args:
        bytes_groesse: Größe in Bytes
    
    Returns:
        Formatierte Größenangabe als String
    """
    if bytes_groesse < 1024:
        return f"{bytes_groesse} Bytes"
    elif bytes_groesse < 1024 * 1024:
        return f"{bytes_groesse / 1024:.2f} KB ({bytes_groesse} Bytes)"
    else:
        return f"{bytes_groesse / (1024 * 1024):.2f} MB ({bytes_groesse} Bytes)"


def main():
    """
    Hauptfunktion des Programms.
    """
    # Dateiname und Inhalt definieren
    dateiname = "beispiel_datei.txt"
    inhalt = """Dies ist eine Beispieldatei.
Sie enthält mehrere Zeilen Text.

Hier sind einige interessante Fakten:
- Python ist eine großartige Programmiersprache
- Fehlerbehandlung ist wichtig für robuste Programme
- UTF-8 ermöglicht Umlaute wie ä, ö, ü und ß

Ende der Datei."""

    print("=" * 60)
    print("Datei-Erstellungs- und Analyse-Programm")
    print("=" * 60)
    print()

    # Schritt 1: Datei erstellen
    print("[1] Datei erstellen...")
    if not datei_erstellen(dateiname, inhalt):
        print("\nProgramm wird aufgrund von Fehlern beendet.")
        return 1
    print()

    # Schritt 2: Dateigröße ermitteln
    print("[2] Dateigröße ermitteln...")
    groesse = dateigroesse_ermitteln(dateiname)
    if groesse is None:
        print("\nProgramm wird aufgrund von Fehlern beendet.")
        return 1
    
    print(f"✓ Dateigröße: {groesse_formatieren(groesse)}")
    print()

    # Schritt 3: Dateiinhalt lesen und anzeigen
    print("[3] Dateiinhalt lesen...")
    gelesener_inhalt = dateiinhalt_lesen(dateiname)
    if gelesener_inhalt is None:
        print("\nProgramm wird aufgrund von Fehlern beendet.")
        return 1
    
    print(f"✓ Inhalt erfolgreich gelesen ({len(gelesener_inhalt)} Zeichen)")
    print()
    
    # Inhalt anzeigen
    print("-" * 60)
    print("DATEIINHALT:")
    print("-" * 60)
    print(gelesener_inhalt)
    print("-" * 60)
    print()
    
    # Zusammenfassung
    print("=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Dateiname:     {dateiname}")
    print(f"Dateigröße:    {groesse_formatieren(groesse)}")
    print(f"Zeichenanzahl: {len(gelesener_inhalt)}")
    print(f"Zeilenanzahl:  {gelesener_inhalt.count(chr(10)) + 1}")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nProgramm wurde vom Benutzer abgebrochen.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Kritischer Fehler: {e}", file=sys.stderr)
        sys.exit(1)