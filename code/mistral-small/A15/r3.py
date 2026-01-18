import http.client
import json

def send_request(host, path, method="GET", headers=None, body=None):
    # Connect to the server
    conn = http.client.HTTPConnection(host)

    try:
        # Send the request
        if method == "POST" and body is not None:
            conn.request(method, path, body, headers)
        else:
            conn.request(method, path, headers=headers)

        # Get the response
        response = conn.getresponse()

        # Check for timeout or error
        if response.status != 200:
            raise Exception(f"Request failed with status code {response.status}")

        # Parse the response
        data = response.read().decode('utf-8')

        try:
            # Try to parse JSON data
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError:
            # If it's not JSON, just return the raw data
            return data
    except Exception as e:
        raise e
    finally:
        conn.close()

# Example usage
if __name__ == "__main__":
    host = "jsonplaceholder.typicode.com"  # Example API endpoint
    path = "/posts/1"

    try:
        data = send_request(host, path)
        print("Response Data:", data)
    except Exception as e:
        print("Error:", e)