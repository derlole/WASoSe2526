#!/usr/bin/env python3
"""
Netzwerk-Request-Programm
Sendet HTTP-Requests und analysiert die Antworten ohne schwere Frameworks.
"""

import urllib.request
import urllib.error
import urllib.parse
import json
import socket
from typing import Dict, Optional, Any
from datetime import datetime


class NetworkClient:
    """Leichtgewichtiger HTTP-Client mit Fehlerbehandlung"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialisiert den Client.
        
        Args:
            timeout: Timeout in Sekunden für Requests
        """
        self.timeout = timeout
        self.default_headers = {
            'User-Agent': 'Python-NetworkClient/1.0'
        }
    
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Führt einen GET-Request durch.
        
        Args:
            url: Die anzufragende URL
            headers: Optional zusätzliche HTTP-Header
            
        Returns:
            Dictionary mit Response-Daten
        """
        return self._make_request(url, method='GET', headers=headers)
    
    def post(self, url: str, data: Optional[Dict] = None, 
             headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Führt einen POST-Request durch.
        
        Args:
            url: Die anzufragende URL
            data: Daten für den Request-Body
            headers: Optional zusätzliche HTTP-Header
            
        Returns:
            Dictionary mit Response-Daten
        """
        return self._make_request(url, method='POST', data=data, headers=headers)
    
    def _make_request(self, url: str, method: str = 'GET', 
                     data: Optional[Dict] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Interne Methode zum Durchführen von HTTP-Requests.
        
        Args:
            url: Die anzufragende URL
            method: HTTP-Methode (GET, POST, etc.)
            data: Optional Daten für Request-Body
            headers: Optional HTTP-Header
            
        Returns:
            Dictionary mit Response-Informationen
        """
        result = {
            'success': False,
            'url': url,
            'method': method,
            'status_code': None,
            'headers': {},
            'body': None,
            'parsed_json': None,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Merge headers
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Prepare request data
            request_data = None
            if data:
                if isinstance(data, dict):
                    request_data = json.dumps(data).encode('utf-8')
                    request_headers['Content-Type'] = 'application/json'
                else:
                    request_data = data.encode('utf-8') if isinstance(data, str) else data
            
            # Create request
            req = urllib.request.Request(
                url,
                data=request_data,
                headers=request_headers,
                method=method
            )
            
            # Make request with timeout
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result['success'] = True
                result['status_code'] = response.status
                result['headers'] = dict(response.headers)
                
                # Read response body
                body = response.read()
                
                # Try to decode as UTF-8
                try:
                    result['body'] = body.decode('utf-8')
                except UnicodeDecodeError:
                    result['body'] = body.decode('latin-1')
                
                # Try to parse as JSON
                if 'application/json' in result['headers'].get('Content-Type', ''):
                    try:
                        result['parsed_json'] = json.loads(result['body'])
                    except json.JSONDecodeError:
                        pass
                
        except urllib.error.HTTPError as e:
            result['error'] = f'HTTP Error {e.code}: {e.reason}'
            result['status_code'] = e.code
            try:
                error_body = e.read().decode('utf-8')
                result['body'] = error_body
            except:
                pass
                
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                result['error'] = f'Request timeout after {self.timeout} seconds'
            else:
                result['error'] = f'URL Error: {e.reason}'
                
        except socket.timeout:
            result['error'] = f'Socket timeout after {self.timeout} seconds'
            
        except Exception as e:
            result['error'] = f'Unexpected error: {type(e).__name__}: {str(e)}'
        
        return result
    
    def analyze_response(self, response: Dict[str, Any]) -> str:
        """
        Analysiert eine Response und erstellt einen Bericht.
        
        Args:
            response: Response-Dictionary von _make_request
            
        Returns:
            Formatierter Analyse-String
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"REQUEST ANALYSIS - {response['timestamp']}")
        lines.append("=" * 70)
        lines.append(f"URL: {response['url']}")
        lines.append(f"Method: {response['method']}")
        lines.append(f"Status: {'SUCCESS' if response['success'] else 'FAILED'}")
        
        if response['status_code']:
            lines.append(f"Status Code: {response['status_code']}")
        
        if response['error']:
            lines.append(f"\n❌ ERROR: {response['error']}")
        
        if response['headers']:
            lines.append("\nRESPONSE HEADERS:")
            for key, value in response['headers'].items():
                lines.append(f"  {key}: {value}")
        
        if response['parsed_json']:
            lines.append("\nPARSED JSON DATA:")
            lines.append(json.dumps(response['parsed_json'], indent=2))
        elif response['body']:
            lines.append("\nRESPONSE BODY:")
            body_preview = response['body'][:500]
            if len(response['body']) > 500:
                body_preview += "... (truncated)"
            lines.append(body_preview)
        
        lines.append("=" * 70)
        return "\n".join(lines)


def extract_data_from_json(json_data: Dict, *keys) -> Dict[str, Any]:
    """
    Extrahiert spezifische Daten aus JSON.
    
    Args:
        json_data: JSON-Dictionary
        *keys: Zu extrahierende Keys
        
    Returns:
        Dictionary mit extrahierten Daten
    """
    extracted = {}
    for key in keys:
        if key in json_data:
            extracted[key] = json_data[key]
    return extracted


def main():
    """Hauptfunktion mit Beispiel-Verwendungen"""
    
    print("🌐 Netzwerk-Request-Programm\n")
    
    # Client initialisieren
    client = NetworkClient(timeout=10)
    
    # Beispiel 1: GET-Request zu einer JSON-API
    print("📡 Beispiel 1: GET-Request zu JSONPlaceholder API")
    print("-" * 70)
    
    response = client.get("https://jsonplaceholder.typicode.com/posts/1")
    print(client.analyze_response(response))
    
    if response['parsed_json']:
        # Daten extrahieren
        extracted = extract_data_from_json(
            response['parsed_json'], 
            'userId', 'id', 'title'
        )
        print("\n📊 Extrahierte Daten:")
        for key, value in extracted.items():
            print(f"  {key}: {value}")
    
    print("\n")
    
    # Beispiel 2: POST-Request
    print("📡 Beispiel 2: POST-Request mit JSON-Daten")
    print("-" * 70)
    
    post_data = {
        'title': 'Test Post',
        'body': 'Dies ist ein Test-Beitrag',
        'userId': 1
    }
    
    response = client.post(
        "https://jsonplaceholder.typicode.com/posts",
        data=post_data
    )
    print(client.analyze_response(response))
    
    print("\n")
    
    # Beispiel 3: Fehlerbehandlung - ungültige URL
    print("📡 Beispiel 3: Fehlerbehandlung - ungültige URL")
    print("-" * 70)
    
    response = client.get("https://this-domain-definitely-does-not-exist-12345.com")
    print(client.analyze_response(response))
    
    print("\n")
    
    # Beispiel 4: Fehlerbehandlung - 404 Error
    print("📡 Beispiel 4: Fehlerbehandlung - HTTP 404")
    print("-" * 70)
    
    response = client.get("https://jsonplaceholder.typicode.com/posts/99999999")
    print(client.analyze_response(response))
    
    print("\n")
    
    # Beispiel 5: Request mit Custom Headers
    print("📡 Beispiel 5: Request mit benutzerdefinierten Headers")
    print("-" * 70)
    
    custom_headers = {
        'Accept': 'application/json',
        'X-Custom-Header': 'MyValue'
    }
    
    response = client.get(
        "https://httpbin.org/headers",
        headers=custom_headers
    )
    print(client.analyze_response(response))
    
    print("\n✅ Alle Beispiele abgeschlossen!")


if __name__ == "__main__":
    main()