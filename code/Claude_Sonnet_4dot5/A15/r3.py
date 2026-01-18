#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Netzwerk-Request-Programm mit Response-Analyse
Verwendet nur Python Standard-Bibliotheken (urllib)
"""

import urllib.request
import urllib.error
import urllib.parse
import json
import socket
from typing import Dict, Any, Optional
from datetime import datetime


class NetworkRequest:
    """Klasse für HTTP-Requests mit Response-Analyse"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialisierung
        
        Args:
            timeout: Timeout in Sekunden für Requests
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
        Sendet einen HTTP-Request und analysiert die Response
        
        Args:
            url: Die Ziel-URL
            method: HTTP-Methode (GET, POST, PUT, DELETE)
            data: Optional - Daten für POST/PUT Requests
            headers: Optional - Zusätzliche HTTP-Headers
            
        Returns:
            Dictionary mit Request-Informationen und Response-Daten
        """
        start_time = datetime.now()
        result = {
            'success': False,
            'url': url,
            'method': method,
            'request_time': None,
            'status_code': None,
            'headers': {},
            'body': None,
            'parsed_data': None,
            'error': None
        }
        
        try:
            # Headers zusammenführen
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Request-Daten vorbereiten
            request_data = None
            if data:
                if isinstance(data, dict):
                    request_data = json.dumps(data).encode('utf-8')
                    request_headers['Content-Type'] = 'application/json'
                else:
                    request_data = data.encode('utf-8') if isinstance(data, str) else data
            
            # Request erstellen
            request = urllib.request.Request(
                url,
                data=request_data,
                headers=request_headers,
                method=method
            )
            
            # Request senden mit Timeout
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                # Response-Informationen sammeln
                result['status_code'] = response.status
                result['headers'] = dict(response.headers)
                
                # Response-Body lesen
                body = response.read()
                
                # Encoding bestimmen
                encoding = response.headers.get_content_charset('utf-8')
                result['body'] = body.decode(encoding)
                
                # Response parsen
                result['parsed_data'] = self._parse_response(
                    result['body'], 
                    result['headers'].get('Content-Type', '')
                )
                
                result['success'] = True
        
        except urllib.error.HTTPError as e:
            # HTTP-Fehler (4xx, 5xx)
            result['status_code'] = e.code
            result['headers'] = dict(e.headers)
            result['error'] = f"HTTP Error {e.code}: {e.reason}"
            try:
                result['body'] = e.read().decode('utf-8')
            except:
                pass
        
        except urllib.error.URLError as e:
            # URL-Fehler (z.B. DNS-Fehler, Verbindungsfehler)
            if isinstance(e.reason, socket.timeout):
                result['error'] = f"Timeout nach {self.timeout} Sekunden"
            else:
                result['error'] = f"URL Error: {e.reason}"
        
        except socket.timeout:
            result['error'] = f"Socket Timeout nach {self.timeout} Sekunden"
        
        except Exception as e:
            result['error'] = f"Unerwarteter Fehler: {type(e).__name__}: {str(e)}"
        
        finally:
            # Request-Zeit berechnen
            end_time = datetime.now()
            result['request_time'] = (end_time - start_time).total_seconds()
        
        return result
    
    def _parse_response(self, body: str, content_type: str) -> Any:
        """
        Parst die Response basierend auf Content-Type
        
        Args:
            body: Response-Body als String
            content_type: Content-Type Header
            
        Returns:
            Geparste Daten (dict für JSON, sonst String)
        """
        try:
            # JSON parsen
            if 'application/json' in content_type.lower():
                return json.loads(body)
            
            # HTML/XML - grundlegende Analyse
            elif 'text/html' in content_type.lower() or 'text/xml' in content_type.lower():
                return {
                    'type': 'html/xml',
                    'length': len(body),
                    'title': self._extract_title(body) if 'html' in content_type.lower() else None
                }
            
            # Plain text
            else:
                return {
                    'type': 'text',
                    'length': len(body),
                    'preview': body[:200] if len(body) > 200 else body
                }
        
        except json.JSONDecodeError:
            return {
                'type': 'invalid_json',
                'error': 'JSON parsing failed',
                'raw': body[:200]
            }
        except Exception as e:
            return {
                'type': 'parsing_error',
                'error': str(e)
            }
    
    def _extract_title(self, html: str) -> Optional[str]:
        """Extrahiert den Titel aus HTML (einfache Methode ohne Parser)"""
        try:
            start = html.lower().find('<title>')
            if start == -1:
                return None
            start += 7
            end = html.lower().find('</title>', start)
            if end == -1:
                return None
            return html[start:end].strip()
        except:
            return None
    
    def analyze_response(self, response: Dict[str, Any]) -> None:
        """
        Gibt eine detaillierte Analyse der Response aus
        
        Args:
            response: Response-Dictionary von send_request()
        """
        print("=" * 70)
        print("NETZWERK-REQUEST ANALYSE")
        print("=" * 70)
        
        print(f"\n🌐 URL: {response['url']}")
        print(f"📤 Methode: {response['method']}")
        print(f"⏱️  Request-Zeit: {response['request_time']:.3f} Sekunden")
        
        if response['success']:
            print(f"✅ Status: Erfolgreich (HTTP {response['status_code']})")
        else:
            print(f"❌ Status: Fehlgeschlagen")
            print(f"🚫 Fehler: {response['error']}")
        
        if response['status_code']:
            print(f"\n📊 HTTP Status Code: {response['status_code']}")
        
        if response['headers']:
            print(f"\n📋 Response Headers ({len(response['headers'])} items):")
            for key, value in list(response['headers'].items())[:5]:
                print(f"   • {key}: {value}")
            if len(response['headers']) > 5:
                print(f"   ... und {len(response['headers']) - 5} weitere")
        
        if response['parsed_data']:
            print(f"\n🔍 Geparste Daten:")
            if isinstance(response['parsed_data'], dict):
                for key, value in list(response['parsed_data'].items())[:5]:
                    value_str = str(value)[:60]
                    print(f"   • {key}: {value_str}")
                if len(response['parsed_data']) > 5:
                    print(f"   ... und {len(response['parsed_data']) - 5} weitere Felder")
            else:
                print(f"   {response['parsed_data']}")
        
        print("\n" + "=" * 70)


def main():
    """Beispiel-Verwendung des NetworkRequest-Programms"""
    
    print("Netzwerk-Request Programm - Demo\n")
    
    # NetworkRequest-Instanz erstellen
    client = NetworkRequest(timeout=10)
    
    # Beispiel 1: GET Request zu einer JSON-API
    print("Test 1: JSON-API Request")
    print("-" * 70)
    response1 = client.send_request(
        'https://jsonplaceholder.typicode.com/posts/1',
        method='GET'
    )
    client.analyze_response(response1)
    
    # Beispiel 2: POST Request mit Daten
    print("\n\nTest 2: POST Request mit JSON-Daten")
    print("-" * 70)
    post_data = {
        'title': 'Test Post',
        'body': 'Dies ist ein Test',
        'userId': 1
    }
    response2 = client.send_request(
        'https://jsonplaceholder.typicode.com/posts',
        method='POST',
        data=post_data
    )
    client.analyze_response(response2)
    
    # Beispiel 3: Request mit Custom Headers
    print("\n\nTest 3: Request mit benutzerdefinierten Headers")
    print("-" * 70)
    custom_headers = {
        'Accept-Language': 'de-DE',
        'Custom-Header': 'TestValue'
    }
    response3 = client.send_request(
        'https://httpbin.org/headers',
        headers=custom_headers
    )
    client.analyze_response(response3)
    
    # Beispiel 4: Timeout-Test
    print("\n\nTest 4: Timeout-Test (kurzes Timeout)")
    print("-" * 70)
    short_timeout_client = NetworkRequest(timeout=0.001)
    response4 = short_timeout_client.send_request(
        'https://jsonplaceholder.typicode.com/posts/1'
    )
    client.analyze_response(response4)
    
    # Beispiel 5: Fehlerbehandlung - ungültige URL
    print("\n\nTest 5: Fehlerbehandlung - ungültige URL")
    print("-" * 70)
    response5 = client.send_request(
        'https://diese-url-existiert-definitiv-nicht-12345.com'
    )
    client.analyze_response(response5)


if __name__ == '__main__':
    main()