#!/usr/bin/env python3
"""
JSON Name Extractor
Extrahiert alle Werte des Attributs "name" aus einer JSON-Datei,
inklusive verschachtelter Strukturen.
"""

import json
import sys
from typing import Any, List


def extract_names(data: Any, names: List[str] = None) -> List[str]:
    """
    Rekursiv alle 'name'-Werte aus einer JSON-Struktur extrahieren.
    
    Args:
        data: Die zu durchsuchende Datenstruktur (dict, list, oder primitiv)
        names: Akkumulator-Liste für gefundene Namen
    
    Returns:
        Liste aller gefundenen 'name'-Werte
    """
    if names is None:
        names = []
    
    if isinstance(data, dict):
        # Wenn das aktuelle Dict ein 'name'-Attribut hat, füge es hinzu
        if 'name' in data:
            names.append(data['name'])
        
        # Rekursiv alle Werte des Dicts durchsuchen
        for value in data.values():
            extract_names(value, names)
    
    elif isinstance(data, list):
        # Rekursiv alle Elemente der Liste durchsuchen
        for item in data:
            extract_names(item, names)
    
    return names


def extract_names_from_file(filepath: str) -> List[str]:
    """
    Liest eine JSON-Datei und extrahiert alle 'name'-Werte.
    
    Args:
        filepath: Pfad zur JSON-Datei
    
    Returns:
        Liste aller gefundenen 'name'-Werte
    
    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert
        json.JSONDecodeError: Wenn die Datei kein gültiges JSON enthält
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return extract_names(data)
    except FileNotFoundError:
        print(f"Fehler: Datei '{filepath}' nicht gefunden.", file=sys.stderr)
        raise
    except json.JSONDecodeError as e:
        print(f"Fehler: Ungültiges JSON in '{filepath}': {e}", file=sys.stderr)
        raise


def main():
    """Hauptfunktion für Kommandozeilen-Nutzung."""
    if len(sys.argv) < 2:
        print("Verwendung: python json_name_extractor.py <json-datei>")
        print("\nBeispiel:")
        print("  python json_name_extractor.py data.json")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        names = extract_names_from_file(filepath)
        
        if names:
            print(f"Gefundene {len(names)} 'name'-Werte:")
            print("-" * 50)
            for i, name in enumerate(names, 1):
                print(f"{i}. {name}")
        else:
            print("Keine 'name'-Attribute gefunden.")
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()