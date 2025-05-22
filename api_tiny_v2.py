import requests
import json

def incluir_nota_servico(TOKEN_TINY, pedido, percentual_iss):
    nfse = json.dumps({
        'nota_servico': {
            'cliente': {
                'codigo': pedido['cliente']['codigo'],
                'nome': pedido['cliente']['nome'],
                'tipo_pessoa': pedido['cliente']['tipoPessoa'],
                'cpf_cnpj': pedido['cliente']['cpfCnpj'],
                'endereco': pedido['cliente']['endereco']['endereco'],
                'numero': pedido['cliente']['endereco']['numero'],
                'complemento': pedido['cliente']['endereco']['complemento'],
                'bairro': pedido['cliente']['endereco']['bairro'],
                'cep': pedido['cliente']['endereco']['cep'],
                'cidade': pedido['cliente']['endereco']['municipio'],
                'uf': pedido['cliente']['endereco']['uf'],
                'fone': pedido['cliente']['telefone'],
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
    print(response)
    print(response.text)
    return response.json()

def enviar_nota_servico(TOKEN_TINY, id_nota):
    url = f'https://api.tiny.com.br/api2/nota.servico.enviar.php?token={TOKEN_TINY}&formato=json&id={id_nota}&enviarEmail=N'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = ''

    response = requests.request('POST', url, headers=headers, data=payload)
    print(response)
    print(response.text)
    return response.json()
