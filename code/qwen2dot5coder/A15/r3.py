import requests

def fetch_and_parse(url):
    try:
        response = requests.get(url, timeout=5)  # Set timeout for the request
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        if 'application/json' in response.headers['Content-Type']:
            data = response.json()  # Parse JSON response
        else:
            print("The response is not in JSON format.")
            return None
        
        # Example of extracting data: Let's assume we want to extract a list of items from the JSON response.
        if 'items' in data:
            items = data['items']
            for item in items:
                print(item)
        else:
            print("No 'items' key found in the response.")
    
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

# Example usage
fetch_and_parse('https://api.example.com/data')