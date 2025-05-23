import requests
import json
import time

def get_orders_v3(ACCESS_TOKEN, PARAMS):
    offset = 0
    total = 100
    lista_pedidos = []

    url_params = ''
    for key, value in PARAMS.items():
        url_params += f'{key}={value}&'

    while offset < total:
        try:
            url = f'https://api.tiny.com.br/public-api/v3/pedidos?{url_params}offset={offset}'

            payload = ''
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            response = response.json()

            offset = offset + 100
            total = response['paginacao']['total']

            lista_pedidos = [*lista_pedidos, *response['itens']]
        except Exception as e:
            print(e)
            time.sleep(5)
    
    return lista_pedidos

def get_markers_v3(ACCESS_TOKEN, id_pedido):
    url = f'https://api.tiny.com.br/public-api/v3/pedidos/{id_pedido}/marcadores'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers)
    response = response.json()
    return response

def add_markers_v3(ACCESS_TOKEN, id_pedido, marcadores):
    url = f'https://api.tiny.com.br/public-api/v3/pedidos/{id_pedido}/marcadores'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    payload = json.dumps(marcadores)

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
