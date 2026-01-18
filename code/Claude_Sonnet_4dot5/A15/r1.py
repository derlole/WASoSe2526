#!/usr/bin/env python3
"""
Netzwerk-Request Programm mit Response-Analyse
Verwendet nur Python Standard-Bibliothek (urllib)
"""

import urllib.request
import urllib.error
import urllib.parse
import json
import socket
from typing import Dict, Any, Optional, List
from datetime import datetime


class NetworkRequest:
    """Klasse für HTTP-Requests mit Fehlerbehandlung und Parsing"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialisiert den NetworkRequest Handler
        
        Args:
            timeout: Timeout für Requests in Sekunden (Standard: 10)
        """
        self.timeout = timeout
        self.default_headers = {
            'User-Agent': 'Python-NetworkRequest/1.0',
            'Accept': 'application/json, text/html, */*'
        }
    
    def send_request(
        self, 
        url: str, 
        method: str = 'GET',
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Sendet einen HTTP-Request und gibt die analysierte Antwort zurück
        
        Args:
            url: Die Ziel-URL
            method: HTTP-Methode (GET, POST, PUT, DELETE, etc.)
            data: Optional - Daten für POST/PUT Requests
            headers: Optional - zusätzliche HTTP-Header
            
        Returns:
            Dictionary mit Response-Daten und Metainformationen
        """
        result = {
            'success': False,
            'url': url,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'status_code': None,
            'headers': {},
            'body': None,
            'parsed_data': None,
            'error': None,
            'response_time_ms': None
        }
        
        try:
            # Header zusammenführen
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Request-Daten vorbereiten
            request_data = None
            if data:
                if method in ['POST', 'PUT', 'PATCH']:
                    request_data = json.dumps(data).encode('utf-8')
                    request_headers['Content-Type'] = 'application/json'
            
            # Request-Objekt erstellen
            request = urllib.request.Request(
                url,
                data=request_data,
                headers=request_headers,
                method=method
            )
            
            # Request senden und Zeit messen
            start_time = datetime.now()
            
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                # Response-Informationen sammeln
                result['success'] = True
                result['status_code'] = response.status
                result['headers'] = dict(response.headers)
                result['response_time_ms'] = round(response_time, 2)
                
                # Body lesen
                body = response.read()
                
                # Body dekodieren
                encoding = response.headers.get_content_charset('utf-8')
                result['body'] = body.decode(encoding)
                
                # Daten parsen (JSON, wenn möglich)
                result['parsed_data'] = self._parse_response(
                    result['body'], 
                    response.headers.get_content_type()
                )
        
        except urllib.error.HTTPError as e:
            # HTTP-Fehler (4xx, 5xx)
            result['error'] = f'HTTP Error {e.code}: {e.reason}'
            result['status_code'] = e.code
            try:
                error_body = e.read().decode('utf-8')
                result['body'] = error_body
                result['parsed_data'] = self._parse_response(
                    error_body, 
                    e.headers.get_content_type() if e.headers else None
                )
            except:
                pass
                
        except urllib.error.URLError as e:
            # Netzwerk-Fehler (DNS, Connection, etc.)
            if isinstance(e.reason, socket.timeout):
                result['error'] = f'Timeout nach {self.timeout} Sekunden'
            else:
                result['error'] = f'URL Error: {e.reason}'
                
        except socket.timeout:
            result['error'] = f'Socket Timeout nach {self.timeout} Sekunden'
            
        except Exception as e:
            # Sonstige Fehler
            result['error'] = f'Unerwarteter Fehler: {type(e).__name__}: {str(e)}'
        
        return result
    
    def _parse_response(self, body: str, content_type: Optional[str]) -> Any:
        """
        Parst den Response-Body basierend auf Content-Type
        
        Args:
            body: Der Response-Body als String
            content_type: Der Content-Type Header
            
        Returns:
            Geparste Daten oder None
        """
        if not body:
            return None
        
        try:
            # JSON parsen
            if content_type and 'json' in content_type.lower():
                return json.loads(body)
            
            # Versuche JSON-Parsing auch ohne expliziten Content-Type
            try:
                return json.loads(body)
            except:
                pass
            
            # HTML/Text einfach zurückgeben
            return body
            
        except json.JSONDecodeError as e:
            return {'parse_error': f'JSON Decode Error: {str(e)}', 'raw': body[:200]}
        except Exception as e:
            return {'parse_error': f'Parse Error: {str(e)}'}
    
    def extract_data(self, parsed_data: Any, path: str) -> Any:
        """
        Extrahiert spezifische Daten aus geparsten Responses
        
        Args:
            parsed_data: Die geparsten Daten (z.B. Dictionary)
            path: Pfad zu den Daten (z.B. "user.name" oder "items[0].id")
            
        Returns:
            Die extrahierten Daten oder None
        """
        if not parsed_data or not isinstance(parsed_data, dict):
            return None
        
        try:
            keys = path.split('.')
            current = parsed_data
            
            for key in keys:
                # Array-Index behandeln
                if '[' in key and ']' in key:
                    key_name = key.split('[')[0]
                    index = int(key.split('[')[1].split(']')[0])
                    if key_name:
                        current = current[key_name][index]
                    else:
                        current = current[index]
                else:
                    current = current[key]
            
            return current
        except (KeyError, IndexError, TypeError, ValueError):
            return None
    
    def batch_requests(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Sendet mehrere Requests nacheinander
        
        Args:
            urls: Liste von URLs
            
        Returns:
            Liste von Result-Dictionaries
        """
        results = []
        for url in urls:
            result = self.send_request(url)
            results.append(result)
        return results


def print_result(result: Dict[str, Any], detailed: bool = True) -> None:
    """
    Gibt das Ergebnis formatiert aus
    
    Args:
        result: Das Result-Dictionary
        detailed: Wenn True, werden alle Details angezeigt
    """
    print("\n" + "="*70)
    print(f"URL: {result['url']}")
    print(f"Methode: {result['method']}")
    print(f"Zeitstempel: {result['timestamp']}")
    print(f"Erfolg: {'✓' if result['success'] else '✗'}")
    
    if result['status_code']:
        status_symbol = '✓' if 200 <= result['status_code'] < 300 else '✗'
        print(f"Status Code: {result['status_code']} {status_symbol}")
    
    if result['response_time_ms']:
        print(f"Antwortzeit: {result['response_time_ms']} ms")
    
    if result['error']:
        print(f"❌ Fehler: {result['error']}")
    
    if detailed and result['headers']:
        print("\nResponse Headers:")
        for key, value in list(result['headers'].items())[:5]:
            print(f"  {key}: {value}")
        if len(result['headers']) > 5:
            print(f"  ... und {len(result['headers']) - 5} weitere")
    
    if result['parsed_data']:
        print("\nGeparste Daten:")
        if isinstance(result['parsed_data'], (dict, list)):
            json_str = json.dumps(result['parsed_data'], indent=2, ensure_ascii=False)
            if len(json_str) > 500:
                print(json_str[:500] + "\n  ... (gekürzt)")
            else:
                print(json_str)
        else:
            data_str = str(result['parsed_data'])
            if len(data_str) > 500:
                print(f"  {data_str[:500]}... (gekürzt)")
            else:
                print(f"  {data_str}")
    
    print("="*70)


def demonstrate_basic_usage():
    """Demonstriert die grundlegende Verwendung"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Grundlegende Verwendung")
    print("="*70)
    
    net = NetworkRequest(timeout=10)
    
    # Beispiel mit öffentlicher API
    print("\n[1] GET Request zu öffentlicher API...")
    result = net.send_request('https://api.github.com/users/github')
    print_result(result)
    
    if result['success'] and result['parsed_data']:
        name = net.extract_data(result['parsed_data'], 'name')
        public_repos = net.extract_data(result['parsed_data'], 'public_repos')
        print(f"\n📊 Extrahierte Daten:")
        print(f"   Name: {name}")
        print(f"   Public Repos: {public_repos}")


def demonstrate_post_request():
    """Demonstriert POST Requests"""
    print("\n" + "="*70)
    print("DEMONSTRATION: POST Request")
    print("="*70)
    
    net = NetworkRequest(timeout=10)
    
    print("\n[2] POST Request mit JSON-Daten...")
    result = net.send_request(
        url='https://httpbin.org/post',
        method='POST',
        data={
            'titel': 'Test-Nachricht',
            'inhalt': 'Dies ist ein Test',
            'autor': 'NetworkRequest Bot',
            'timestamp': datetime.now().isoformat()
        }
    )
    print_result(result)


def demonstrate_error_handling():
    """Demonstriert Fehlerbehandlung"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Fehlerbehandlung")
    print("="*70)
    
    # Timeout Test
    print("\n[3] Test: Timeout...")
    net_short = NetworkRequest(timeout=0.001)
    result = net_short.send_request('https://httpbin.org/delay/5')
    print_result(result, detailed=False)
    
    # 404 Error Test
    print("\n[4] Test: 404 Not Found...")
    net = NetworkRequest()
    result = net.send_request('https://httpbin.org/status/404')
    print_result(result, detailed=False)
    
    # 500 Server Error Test
    print("\n[5] Test: 500 Server Error...")
    result = net.send_request('https://httpbin.org/status/500')
    print_result(result, detailed=False)


def demonstrate_data_extraction():
    """Demonstriert Datenextraktion"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Datenextraktion")
    print("="*70)
    
    net = NetworkRequest()
    
    print("\n[6] Abrufen und Extrahieren von verschachtelten Daten...")
    result = net.send_request('https://api.github.com/repos/python/cpython')
    
    if result['success'] and result['parsed_data']:
        # Verschiedene Daten extrahieren
        name = net.extract_data(result['parsed_data'], 'name')
        stars = net.extract_data(result['parsed_data'], 'stargazers_count')
        owner_login = net.extract_data(result['parsed_data'], 'owner.login')
        
        print(f"\n📊 Extrahierte Repository-Daten:")
        print(f"   Name: {name}")
        print(f"   Stars: {stars:,}" if stars else "   Stars: N/A")
        print(f"   Owner: {owner_login}")


def demonstrate_custom_headers():
    """Demonstriert Custom Headers"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Custom Headers")
    print("="*70)
    
    net = NetworkRequest()
    
    print("\n[7] Request mit benutzerdefinierten Headers...")
    result = net.send_request(
        url='https://httpbin.org/headers',
        headers={
            'X-Custom-Header': 'MeinWert',
            'Authorization': 'Bearer fake-token-123'
        }
    )
    print_result(result)


def main():
    """Hauptfunktion mit verschiedenen Demonstrationen"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  NETZWERK-REQUEST PROGRAMM MIT RESPONSE-ANALYSE".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        # Alle Demonstrationen ausführen
        demonstrate_basic_usage()
        demonstrate_post_request()
        demonstrate_error_handling()
        demonstrate_data_extraction()
        demonstrate_custom_headers()
        
        print("\n" + "="*70)
        print("✓ Alle Demonstrationen abgeschlossen!")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Programm wurde unterbrochen.")
    except Exception as e:
        print(f"\n\n❌ Fehler: {e}")


if __name__ == '__main__':
    main()