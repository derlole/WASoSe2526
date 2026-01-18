import http.client
import json
from socket import timeout

def send_request(host, path, method='GET', body=None, headers=None, timeout_duration=10):
    # Wählen Sie das richtige HTTP-Verb (GET oder POST)
    if method == 'POST' and body is None:
        raise ValueError("Body must be provided for POST requests")

    conn = http.client.HTTPSConnection(host, timeout=timeout_duration)

    try:
        # Fügen Sie benutzerdefinierte Header hinzu, falls vorhanden
        if headers:
            conn.request(method, path, body=body, headers=headers)
        else:
            conn.request(method, path, body=body)

        response = conn.getresponse()
        data = response.read().decode('utf-8')
        status_code = response.status

        # Behandeln Sie Fehler basierend auf dem Statuscode
        if status_code >= 400:
            raise Exception(f"HTTP request failed with status code {status_code}: {data}")

        return data, status_code
    except timeout:
        raise Exception("Request timed out")
    finally:
        conn.close()

def parse_response(response):
    try:
        # Versuchen Sie, die Antwort als JSON zu parsen
        parsed_data = json.loads(response)
        return parsed_data
    except json.JSONDecodeError as e:
        raise Exception("Failed to parse response as JSON") from e

def main():
    host = 'jsonplaceholder.typicode.com'
    path = '/posts/1'
    method = 'GET'

    try:
        # Senden Sie den HTTP-Request
        response_data, status_code = send_request(host, path, method)

        # Analysieren Sie die Antwort
        parsed_data = parse_response(response_data)

        # Extrahieren und drucken Sie die relevanten Daten
        print("Response Data:", json.dumps(parsed_data, indent=4))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()