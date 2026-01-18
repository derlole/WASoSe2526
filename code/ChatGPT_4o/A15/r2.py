import http.client
import json
from urllib.parse import urlparse

def fetch_and_parse(url, timeout=5):
    """
    Sendet einen HTTP GET-Request zu einer URL, prüft die Antwort,
    parst JSON und extrahiert Daten.
    
    Args:
        url (str): Ziel-URL
        timeout (int): Timeout in Sekunden für die Anfrage
    
    Returns:
        dict: Geparste JSON-Daten oder None bei Fehler
    """
    try:
        # URL parsen
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or "/"

        if parsed_url.query:
            path += "?" + parsed_url.query

        # HTTP-Verbindung aufbauen
        conn = http.client.HTTPConnection(host, timeout=timeout) if parsed_url.scheme == "http" else http.client.HTTPSConnection(host, timeout=timeout)
        
        # GET-Request senden
        conn.request("GET", path)
        response = conn.getresponse()
        
        # Status prüfen
        if response.status != 200:
            print(f"Fehler: HTTP Status {response.status} {response.reason}")
            return None

        # Response lesen
        data = response.read().decode()
        conn.close()

        # JSON parsen
        parsed_data = json.loads(data)
        return parsed_data

    except http.client.HTTPException as e:
        print(f"HTTP-Fehler: {e}")
    except json.JSONDecodeError:
        print("Fehler beim Parsen von JSON")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")
    
    return None

def extract_field(data, field_name):
    """
    Extrahiert rekursiv alle Werte eines bestimmten Feldes aus verschachteltem JSON.
    """
    results = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k == field_name:
                results.append(v)
            else:
                results.extend(extract_field(v, field_name))
    elif isinstance(data, list):
        for item in data:
            results.extend(extract_field(item, field_name))
    
    return results

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/users"
    json_data = fetch_and_parse(url)

    if json_data:
        print("Rohdaten der Antwort:")
        print(json.dumps(json_data, indent=2))

        # Beispiel: Alle "name"-Felder extrahieren
        names = extract_field(json_data, "name")
        print("\nExtrahierte Namen:")
        print(names)
