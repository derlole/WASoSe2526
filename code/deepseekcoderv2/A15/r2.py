import http.client
import json

def send_request(host, path, method='GET', body=None):
    try:
        # Create a connection to the host
        conn = http.client.HTTPConnection(host, timeout=5)
        
        # Send the request
        if method == 'POST':
            headers = {'Content-type': 'application/json'}
            body_str = json.dumps(body) if isinstance(body, dict) else str(body)
            conn.request('POST', path, body_str, headers)
        elif method == 'GET':
            conn.request('GET', path)
        
        # Get the response
        response = conn.getresponse()
        res_data = response.read().decode("utf-8")
        
        # Parse and return the JSON data if possible
        try:
            parsed_data = json.loads(res_data)
            return parsed_data
        except ValueError as e:
            print("Error parsing JSON:", e)
            return res_data
        
    except http.client.HTTPException as e:
        print("HTTP request failed:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage:
host = 'httpbin.org'
path = '/get'  # Using a simple endpoint for demonstration
response_data = send_request(host, path)
if response_data:
    print("Response data:", response_data)