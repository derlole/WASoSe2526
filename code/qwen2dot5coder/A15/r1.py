import requests

def fetch_data(url):
    try:
        # Send HTTP request with a timeout of 5 seconds
        response = requests.get(url, timeout=5)
        
        # Check if the request was successful
        if response.status_code == 200:
            return parse_response(response.text)
        else:
            print(f"Error: Received status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def parse_response(html):
    # Implement your HTML parsing logic here
    # For example, extract specific elements or data from the HTML response
    # You might use BeautifulSoup for more complex parsing tasks
    
    # Dummy implementation that returns a fixed string
    return "Data parsed from response"

# Example usage
url = 'https://example.com'
parsed_data = fetch_data(url)
print(parsed_data)