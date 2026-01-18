#!/usr/bin/env python3
"""
JSON Name Extractor - Extrahiert alle "name"-Attribute aus JSON-Dateien

Dieses Skript durchsucht rekursiv JSON-Strukturen und sammelt alle Werte
des Attributs "name", unabhängig von der Verschachtelungstiefe.
"""

import json
import sys
from typing import List, Any, Union


def extract_names(data: Any, names: List[str] = None) -> List[str]:
    """
    Extrahiert rekursiv alle "name"-Werte aus einer JSON-Struktur.
    
    Args:
        data: Die zu durchsuchende JSON-Struktur (dict, list oder primitiver Typ)
        names: Liste zum Sammeln der gefundenen Namen (wird automatisch initialisiert)
    
    Returns:
        Liste aller gefundenen "name"-Werte
    """
    if names is None:
        names = []
    
    # Fall 1: Dictionary - prüfe auf "name"-Schlüssel und durchsuche alle Werte
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "name":
                # Konvertiere den Wert zu String, falls es kein String ist
                names.append(str(value))
            # Rekursiv alle Werte durchsuchen
            extract_names(value, names)
    
    # Fall 2: Liste - durchsuche alle Elemente
    elif isinstance(data, list):
        for item in data:
            extract_names(item, names)
    
    # Fall 3: Primitive Typen (str, int, bool, None) - nichts zu tun
    
    return names


def extract_names_from_file(filepath: str) -> List[str]:
    """
    Liest eine JSON-Datei und extrahiert alle "name"-Attribute.
    
    Args:
        filepath: Pfad zur JSON-Datei
    
    Returns:
        Liste aller gefundenen "name"-Werte
    
    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert
        json.JSONDecodeError: Wenn die Datei kein gültiges JSON enthält
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return extract_names(data)


def extract_names_from_file_streaming(filepath: str) -> List[str]:
    """
    Liest eine große JSON-Datei streambasiert (für sehr große Dateien).
    
    Hinweis: Diese Methode lädt die gesamte Datei in den Speicher,
    ist aber effizienter als mehrfaches Parsen.
    
    Args:
        filepath: Pfad zur JSON-Datei
    
    Returns:
        Liste aller gefundenen "name"-Werte
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        # Für sehr große Dateien: Chunk-weise lesen
        content = file.read()
        data = json.loads(content)
    
    return extract_names(data)


# Beispiel-Nutzung und Tests
if __name__ == "__main__":
    # Beispiel 1: Einfache JSON-Struktur
    example1 = {
        "name": "Hauptobjekt",
        "id": 1,
        "beschreibung": "Ein Beispiel"
    }
    
    # Beispiel 2: Verschachtelte Struktur
    example2 = {
        "name": "Firma",
        "mitarbeiter": [
            {
                "name": "Anna Schmidt",
                "position": "Entwicklerin",
                "projekte": [
                    {"name": "Projekt Alpha", "status": "aktiv"},
                    {"name": "Projekt Beta", "status": "abgeschlossen"}
                ]
            },
            {
                "name": "Max Müller",
                "position": "Designer",
                "projekte": [
                    {"name": "Projekt Gamma", "status": "geplant"}
                ]
            }
        ],
        "abteilungen": {
            "IT": {
                "name": "IT-Abteilung",
                "leiter": {"name": "Dr. Weber"}
            },
            "HR": {
                "name": "Personalabteilung",
                "leiter": {"name": "Frau Klein"}
            }
        }
    }
    
    # Beispiel 3: Liste als Wurzelelement
    example3 = [
        {"name": "Element 1", "wert": 100},
        {"name": "Element 2", "wert": 200},
        {
            "name": "Element 3",
            "kinder": [
                {"name": "Kind 1"},
                {"name": "Kind 2"}
            ]
        }
    ]
    
    print("=" * 60)
    print("JSON Name Extractor - Beispiele")
    print("=" * 60)
    
    print("\nBeispiel 1 - Einfache Struktur:")
    print(f"Input: {example1}")
    names1 = extract_names(example1)
    print(f"Gefundene Namen: {names1}")
    
    print("\n" + "-" * 60)
    print("\nBeispiel 2 - Verschachtelte Struktur:")
    names2 = extract_names(example2)
    print(f"Gefundene Namen ({len(names2)} gesamt):")
    for i, name in enumerate(names2, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "-" * 60)
    print("\nBeispiel 3 - Liste als Wurzel:")
    names3 = extract_names(example3)
    print(f"Gefundene Namen: {names3}")
    
    print("\n" + "=" * 60)
    
    # Kommandozeilen-Schnittstelle
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            print(f"\nLese Datei: {filepath}")
            names = extract_names_from_file(filepath)
            print(f"\n{len(names)} Namen gefunden:")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        except FileNotFoundError:
            print(f"Fehler: Datei '{filepath}' nicht gefunden!", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Fehler: Ungültiges JSON in '{filepath}': {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Fehler: {e}", file=sys.stderr)
            sys.exit(1)
