import json
from typing import List, Any

def extract_names(json_data: Any) -> List[str]:
    names = []

    def extract(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "name":
                    names.append(value)
                else:
                    extract(value)
        elif isinstance(obj, list):
            for item in obj:
                extract(item)

    extract(json_data)
    return names

# Beispiel zur Verwendung der Funktion
if __name__ == "__main__":
    with open("example.json", "r") as file:
        json_data = json.load(file)

    names = extract_names(json_data)
    print(names)