import http.client
import json
from urllib.parse import urlparse

def fetch_and_parse(url, timeout=5):
    """
    Sendet einen HTTP-Request und analysiert die JSON-Antwort.
    
    Args:
        url (str): Die URL, die angefragt wird.
        timeout (int): Timeout in Sekunden.
    
    Returns:
        dict: Geparste JSON-Daten oder None bei Fehlern.
    """
    try:
        # URL parsen
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or "/"
        if parsed_url.query:
            path += "?" + parsed_url.query
        
        # Verbindung aufbauen
        connection = http.client.HTTPSConnection(host, timeout=timeout) if parsed_url.scheme == "https" else http.client.HTTPConnection(host, timeout=timeout)
        
        # Request senden
        connection.request("GET", path)
        response = connection.getresponse()
        
        # Status prüfen
        if response.status != 200:
            print(f"Fehler: HTTP {response.status} {response.reason}")
            return None
        
        # Antwort lesen
        data = response.read()
        
        # JSON parsen
        try:
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError:
            print("Fehler: Antwort konnte nicht als JSON geparst werden")
            return None
        
    except Exception as e:
        print(f"Netzwerkfehler: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()

# Beispiel: API-Request an JSONPlaceholder
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/todos/1"
    result = fetch_and_parse(url)
    if result:
        print("Erfolg! Geparste Daten:")
        for key, value in result.items():
            print(f"{key}: {value}")
