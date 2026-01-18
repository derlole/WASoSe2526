import requests

def send_http_request(url, method='GET', data=None, headers={}):
    """
    Sends an HTTP request and returns the response.
    
    Args:
        url (str): The URL to which we're sending a request.
        method (str): 'GET' or 'POST'. Default is 'GET'.
        data (dict): Dictionary containing POST request data. Defaults to None.
        headers (dict): Custom headers. Defaults to an empty dictionary.

    Returns:
        requests.Response: The response from the server.
    """
    try:
        if method == 'GET':
            return requests.get(url, params=data, headers=headers)
        elif method == 'POST':
            return requests.post(url, data=data, headers=headers)
        else:
            print("Invalid request method. Only GET and POST are supported.")
            return None
    except requests.RequestException as e:
        # Handle any exceptions (e.g., ConnectionError, Timeout) that might occur during the request.
        print(f"Request Exception: {e}")
        return None

def parse_response(response):
    """
    Attempts to extract relevant data from the response.

    Args:
        response (requests.Response): The HTTP response.

    Returns:
        dict or str: A dictionary containing parsed data, or a message indicating no data was found.
    """
    if response.status_code == 200:
        try:
            # For example, let's assume we're expecting JSON in our responses.
            return response.json()
        except ValueError:
            print("Failed to parse JSON.")
            return "No data available"
    else:
        print(f"Failed with status code: {response.status_code}")
        return str(response.text)

# Example usage
if __name__ == "__main__":
    url = 'http://example.com/api/endpoint'  # Ein Beispiel-URL; Ersetze durch deine eigene URL.
    
    response = send_http_request(url, method='GET')
    if response:
        print(f"Status Code: {response.status_code}")
        parsed_data = parse_response(response)
        if isinstance(parsed_data, dict):
            print("Parsed Data:", parsed_data)
        else:
            print("Parsed Data:", parsed_data)

    # Timeout beispiel
    try:
        url_with_timeout = 'http://example.com/api/endpoint'
        response_with_timeout = send_http_request(url_with_timeout, method='GET', timeout=5)  # Setze ein Timeout von 5 Sekunden.
        if response_with_timeout:
            parsed_data_with_timeout = parse_response(response_with_timeout)
            print("Parsed Data with Timeout:", parsed_data_with_timeout)
    except requests.Timeout as e:
        print(f"Timeout Exception: {e}")