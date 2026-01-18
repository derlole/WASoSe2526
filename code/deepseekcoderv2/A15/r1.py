import http.client
import json

def send_request(host, path):
    try:
        # Set up a connection to the host
        conn = http.client.HTTPConnection(host, port=80, timeout=5)
        
        # Send a GET request
        conn.request("GET", path)
        
        # Get the response
        response = conn.getresponse()
        raw_data = response.read()
        
        # Parse JSON if the content type is application/json
        if 'application/json' in response.getheader('content-type'):
            data = json.loads(raw_data)
        else:
            data = raw_data.decode("utf-8")
        
        return {
            "status": response.status,
            "reason": response.reason,
            "headers": dict(response.getheaders()),
            "body": data
        }
    
    except http.client.HTTPException as e:
        print("An error occurred:", str(e))
        return None
    finally:
        if 'conn' in locals():
            conn.close()

# Example usage
if __name__ == "__main__":
    host = "api.example.com"
    path = "/data"
    response_info = send_request(host, path)
    
    if response_info:
        print("Response Status:", response_info["status"], response_info["reason"])
        print("Headers:", response_info["headers"])
        print("Body:", response_info["body"])