import urllib.request
from urllib.error import URLError, HTTPError

def send_request(url):
    try:
        # Create a request object
        request = urllib.request.Request(url)

        # Send the request and get the response
        with urllib.request.urlopen(request) as response:
            # Get the status code of the response
            status_code = response.getcode()
            
            # Read the content of the response
            data = response.read()

            # Decode the data from bytes to string assuming UTF-8 encoding
            decoded_data = data.decode('utf-8')

            # Print the status code and the content of the response
            print(f"Status Code: {status_code}")
            print("Response Content:")
            print(decoded_data)

    except HTTPError as e:
        # Handle HTTP errors (e.g., 404, 500)
        print(f"HTTP Error occurred: {e.code} - {e.reason}")
    except URLError as e:
        # Handle URL-related errors (e.g., invalid URL)
        print(f"URL Error occurred: {e.reason}")
    except Exception as e:
        # Handle other possible exceptions
        print(f"An error occurred: {e}")

# Example usage of the function
url = "https://jsonplaceholder.typicode.com/posts/1"
send_request(url)