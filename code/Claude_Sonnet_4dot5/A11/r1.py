#!/usr/bin/env python3
"""
JSON Name Extractor
Liest JSON-Dateien und extrahiert alle Werte des Attributs "name",
auch aus verschachtelten Strukturen.
"""

import json
import sys
from typing import List, Any


def extract_names(data: Any, names: List[str] = None) -> List[str]:
    """
    Rekursive Funktion zum Extrahieren aller "name"-Werte aus einer JSON-Struktur.
    
    Args:
        data: Die zu durchsuchende Datenstruktur (dict, list, oder primitiver Typ)
        names: Liste zum Sammeln der gefundenen Namen
    
    Returns:
        Liste aller gefundenen "name"-Werte
    """
    if names is None:
        names = []
    
    # Fall 1: Dictionary durchsuchen
    if isinstance(data, dict):
        for key, value in data.items():
            # Wenn der Key "name" ist, den Wert zur Liste hinzufügen
            if key == "name":
                names.append(str(value))
            # Rekursiv in den Wert eintauchen
            extract_names(value, names)
    
    # Fall 2: Liste durchsuchen
    elif isinstance(data, list):
        for item in data:
            extract_names(item, names)
    
    # Fall 3: Primitive Typen (str, int, float, bool, None) - nichts zu tun
    
    return names


def extract_names_from_file(filepath: str) -> List[str]:
    """
    Liest eine JSON-Datei und extrahiert alle "name"-Werte.
    
    Args:
        filepath: Pfad zur JSON-Datei
    
    Returns:
        Liste aller gefundenen "name"-Werte
    
    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert
        json.JSONDecodeError: Wenn die Datei kein gültiges JSON enthält
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return extract_names(data)


def main():
    """Hauptfunktion für Kommandozeilen-Nutzung."""
    if len(sys.argv) < 2:
        print("Usage: python json_name_extractor.py <json_file>")
        print("\nExample:")
        print("  python json_name_extractor.py data.json")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        names = extract_names_from_file(filepath)
        
        print(f"Gefundene 'name'-Werte: {len(names)}")
        print("-" * 50)
        for i, name in enumerate(names, 1):
            print(f"{i}. {name}")
        
        return names
    
    except FileNotFoundError:
        print(f"Fehler: Datei '{filepath}' nicht gefunden.")
        sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(f"Fehler: Ungültiges JSON-Format - {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()