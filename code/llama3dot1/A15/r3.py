import socket
import select
import time

# Konstanten für die Anfrage
HOST = 'www.example.com'
PORT = 80
PATH = '/'
METHOD = 'GET'

# Funktion zum senden der Anfrage
def send_request(host, port, path):
    # Erstelle ein Socket-Objekt
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Verbinde mit dem Server
    try:
        sock.connect((host, port))
    except ConnectionRefusedError as e:
        print(f"Verbindung zum Server {host}:{port} konnte nicht hergestellt werden: {e}")
        return
    
    # Bilde den HTTP-Anfrage-String
    request = f"{METHOD} {PATH} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    # Sende die Anfrage
    try:
        sock.sendall(request.encode())
    except Exception as e:
        print(f"Anfrage konnte nicht gesendet werden: {e}")
        return
    
    # Warte auf Antwort (Timeout 5 Sekunden)
    start_time = time.time()
    while True:
        readable, writable, errored = select.select([sock], [], [], 5)
        
        if time.time() - start_time > 5:
            print("Timeout: Keine Antwort vom Server erhalten.")
            return
        
        if sock in readable:
            # Lese die Antwort
            response = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            # Analysiere die Antwort
            lines = response.decode().split('\r\n')
            status_line = lines[0]
            print(status_line)
            
            # Extrahiere Daten (z.B. Status-Code, Inhalts-Type)
            status_code = int(status_line.split(' ')[1])
            content_type = None
            for line in lines:
                if line.startswith('Content-Type: '):
                    content_type = line.split(': ', 1)[1]
            
            print(f"Status-Code: {status_code}")
            print(f"Inhalts-Type: {content_type}")
            
            # Schließe das Socket-Objekt
            sock.close()
            return

# Aufruf der Funktion
send_request(HOST, PORT, PATH)