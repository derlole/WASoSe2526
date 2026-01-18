import http.client
import json

def send_request(host, path):
    try:
        # Create a connection to the host
        conn = http.client.HTTPSConnection(host, 443 if 'https' in host else 80, timeout=5)
        
        # Send request
        conn.request("GET", path)
        
        # Get response
        response = conn.getresponse()
        data = response.read()
        
        # Parse JSON if the content type is application/json
        if 'application/json' in response.getheader('Content-Type'):
            try:
                parsed_data = json.loads(data)
                return parsed_data
            except ValueError as e:
                print("Error parsing JSON:", str(e))
        
        # Return raw data if not JSON
        return data
    
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# Example usage
host = "api.example.com"
path = "/data"
response_data = send_request(host, path)
if response_data:
    if isinstance(response_data, dict):
        print("Parsed JSON data:", json.dumps(response_data, indent=4))
    else:
        print("Raw Data:", response_data.decode('utf-8'))