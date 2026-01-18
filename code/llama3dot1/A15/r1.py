import socket
import http.parser as hp

# Zeiten in Sekunden
TIMEOUT = 5

def request(url):
    try:
        # Erstelle ein Socket-Objekt
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Setze den Timeout
        sock.settimeout(TIMEOUT)
        
        # Verbinde mit dem Zielserver
        print(f"Verbinde zu {url}...")
        sock.connect((url.split('://')[-1].split('/')[0], 80))
        
        # Bilde den Request-String
        method = 'GET'
        path = url.split('://')[-1].split('/')[1]
        query = ''
        http_version = 'HTTP/1.1'
        request_string = f"{method} {path} HTTP/{http_version}\r\nHost: {url.split('://')[-1].split('/')[0]}\r\n\r\n"
        
        # Schreibe den Request-String
        sock.sendall(request_string.encode())
        
        # Lese die Antwort
        response = ''
        chunk_size = 1024
        while True:
            chunk = sock.recv(chunk_size)
            if not chunk:
                break
            response += chunk.decode()
        
        # Schließe das Socket-Objekt
        sock.close()
        
        # Parsediere die Antwort und extrahiere Daten
        parsed_response = hp.parse(response)
        
        return parsed_response
        
    except socket.timeout as e:
        print(f"Zeitüberschreitung: {e}")
        return None
    
    except Exception as e:
        print(f"Fehler: {e}")
        return None

# Beispielaufruf
url = 'http://example.com'
response = request(url)

if response is not None:
    print("Status-Code:", response.status_code)
    print("Header:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")