from configuration.config import BASE_URL
import requests
from utilities.utils import encrypt_data

DEFAULT_HEADERS = {
    "x-api-key": "reqres-free-v1",
    "Content-Type": "application/json"
}

def request(method, endpoint, data=None, headers=None, encrypt=False):
    url = f"{BASE_URL}{endpoint}"
    method = method.upper()
    headers = headers or {}

    # Merge default headers with provided headers
    all_headers = {**DEFAULT_HEADERS, **headers}

    if encrypt and data:
        data = {"payload": encrypt_data(data)}

    if method == "POST":
        response = requests.post(url, json=data, headers=all_headers)
    elif method == "GET":
        response = requests.get(url, headers=all_headers)
    elif method == "PUT":
        response = requests.put(url, json=data, headers=all_headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=all_headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response
