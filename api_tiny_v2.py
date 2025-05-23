import requests
import json
import re

def add_service_invoice(TOKEN_TINY, pedido, percentual_iss):
    def sanitize_string(input_string):
        return re.sub(r'[^a-zA-Z0-9]', '', input_string)

    nfse = json.dumps({
        'nota_servico': {
            'cliente': {
                'codigo': pedido['cliente']['codigo'],
                'nome': sanitize_string(pedido['cliente']['nome']),
                'tipo_pessoa': pedido['cliente']['tipoPessoa'],
                'cpf_cnpj': pedido['cliente']['cpfCnpj'],
                'endereco': sanitize_string(pedido['cliente']['endereco']['endereco']),
                'numero': sanitize_string(pedido['cliente']['endereco']['numero']),
                'complemento': sanitize_string(pedido['cliente']['endereco']['complemento']),
                'bairro': sanitize_string(pedido['cliente']['endereco']['bairro']),
                'cep': sanitize_string(pedido['cliente']['endereco']['cep']),
                'cidade': sanitize_string(pedido['cliente']['endereco']['municipio']),
                'uf': sanitize_string(pedido['cliente']['endereco']['uf']),
                'fone': sanitize_string(pedido['cliente']['telefone']),
                'email': pedido['cliente']['email'],
                'atualizar_cliente': 'N'
            },
            'servico': {
                'descricao': 'Serviço de manipulação',
                'valor_servico': pedido['valor'],
                'codigo_lista_servico': '04.07'
            },
            'percentual_ir': '0',
            'texto_ir': 'IR Isento Cfe. Lei nro. 9430/96 Art.64',
            'percentual_iss': percentual_iss,
            'descontar_iss_total': 'N',
            'codigo_nbs': '1.0203.00.00',
            'cnae': '4771702',
            'crt': 3
        }
    })

    url = f'https://api.tiny.com.br/api2/nota.servico.incluir.php?token={TOKEN_TINY}&formato=json&nota={nfse}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = ''

    response = requests.request('POST', url, headers=headers, data=payload)
    return response.json()

def send_service_invoice(TOKEN_TINY, id_nota):
    url = f'https://api.tiny.com.br/api2/nota.servico.enviar.php?token={TOKEN_TINY}&formato=json&id={id_nota}&enviarEmail=N'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = ''

    response = requests.request('POST', url, headers=headers, data=payload)
    return response
