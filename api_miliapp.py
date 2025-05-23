import requests
import json


def get_tiny_tokens(origin):
    url = f'https://api.fmiligrama.com/tiny/token?sorting='

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    for token in response:
        if token['origin'] == origin:
            access_token = token['access_token']
            refresh_token = token['refresh_token']

    return access_token, refresh_token
