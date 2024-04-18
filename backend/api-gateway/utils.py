import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_request(method, url, data=None, params=None):
    """
    Sends a HTTP request to the specified URL.
    
    Args:
        method (str): The HTTP method to use.
        url (str): The URL to send the request to.
        data (dict, optional): The JSON data to send with the request.
        params (dict, optional): The parameters to append in the request URL.

    Returns:
        dict: A dictionary with the response data and status code.
    """
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.request(method, url, headers=headers, json=data, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
        return {"data": response.json(), "status": response.status_code}
    except requests.HTTPError as e:
        logger.error("HTTP error occurred: %s", e)
        return {"error": f"HTTP error: {str(e)}", "status": response.status_code}
    except requests.RequestException as e:
        logger.error("Error in request: %s", e)
        return {"error": str(e), "status": None}
    except ValueError:  # Includes simplejson.decoder.JSONDecodeError
        logger.error("Decoding JSON has failed")
        return {"error": "Decoding JSON has failed", "status": response.status_code}
    except Exception as e:
        logger.error("An error occurred: %s", e)
        return {"error": str(e), "status": None}

# Example uses
def get(url, params=None):
    return send_request('GET', url, params=params)

def post(url, data):
    return send_request('POST', url, data=data)

def put(url, data):
    return send_request('PUT', url, data=data)

def delete(url):
    return send_request('DELETE', url)
