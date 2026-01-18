import requests
from requests.exceptions import Timeout, RequestException

def send_request(url):
    try:
        # Set a timeout for the request
        response = requests.get(url, timeout=10)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request was successful!")
            return response.json()  # Parse JSON response
        else:
            print(f"Failed to retrieve data: HTTP Status Code {response.status_code}")
    except Timeout:
        print("The request timed out.")
    except RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Example URL to test with
    data = send_request(url)

    if data:
        print("Extracted Data:", data)