import http.client
import json
from urllib.parse import urlparse

def fetch_and_parse(url, timeout=5):
    """
    Sendet einen HTTP GET-Request an die angegebene URL,
    parst die JSON-Antwort und gibt die extrahierten Daten zurück.
    """
    try:
        # URL zerlegen
        parsed_url = urlparse(url)
        conn = None

        # Verbindung erstellen (HTTP oder HTTPS)
        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(parsed_url.netloc, timeout=timeout)
        else:
            conn = http.client.HTTPConnection(parsed_url.netloc, timeout=timeout)

        # Request senden
        path = parsed_url.path or "/"
        if parsed_url.query:
            path += "?" + parsed_url.query
        conn.request("GET", path)

        # Response erhalten
        response = conn.getresponse()
        status = response.status
        data = response.read().decode('utf-8')

        if status != 200:
            raise Exception(f"HTTP Error {status}: {response.reason}")

        # Versuchen, JSON zu parsen
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            raise Exception("Antwort ist kein gültiges JSON")

        # Beispiel: Alle Werte mit Schlüssel "name" extrahieren
        extracted_names = []
        def extract_names(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "name":
                        extracted_names.append(v)
                    extract_names(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_names(item)

        extract_names(json_data)
        return extracted_names

    except Exception as e:
        print(f"Fehler beim Abrufen der URL: {e}")
        return None
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/users"  # Beispiel-API
    names = fetch_and_parse(url)
    if names:
        print("Gefundene Namen:", names)
    else:
        print("Keine Daten extrahiert.")
