import os
import time
from dotenv import load_dotenv
import datetime
from api_tiny_v3 import obter_pedidos_v3, obter_marcadores_v3, incluir_marcadores_v3
from api_miliapp import obter_tokens_tiny
from api_tiny_v2 import incluir_nota_servico, enviar_nota_servico


load_dotenv()
TOKEN_TINY_CWB = os.getenv('TOKEN_TINY_CWB')
TOKEN_TINY_FOR = os.getenv('TOKEN_TINY_FOR')


def main():
    os.system('cls')
    origins = ['miligrama', 'miligrama_nordeste']

    for origin in origins:
        if origin == 'miligrama':
            access_token, refresh_token = obter_tokens_tiny(origin)
            token_tiny = TOKEN_TINY_CWB
            percentual_iss = '5'
        elif origin == 'miligrama_nordeste':
            access_token, refresh_token = obter_tokens_tiny(origin)
            token_tiny = TOKEN_TINY_FOR
            percentual_iss = '3'

        print('Obtendo lista de pedidos')
        parametros_busca = {
            # 'situacao': 3, # Aprovado
            # 'numero': '268533',
            'orderBy': 'asc',
            'dataInicial': '2025-05-21',
            'dataFinal': '2025-05-21',
        }
        lista_pedidos = obter_pedidos_v3(access_token, parametros_busca)

        k = 0
        for pedido in lista_pedidos:
            k += 1
            print(f'===== origin: {origin} => {k} / {len(lista_pedidos)} =====')
            print(pedido['numeroPedido'])
            
            id_pedido = pedido['id']
            situacao = pedido['situacao']
            if situacao == 8 or situacao == 0 or situacao == 2:
                print('Pedido não está aprovado, pulando...')
                continue
            else:
                print('Buscando marcadores')
                while True:
                    try:
                        marcadores = obter_marcadores_v3(access_token, id_pedido)
                        print(marcadores)
                        break
                    except:
                        print('Erro ao buscar marcadores')
                        time.sleep(1)

                nfse_emitida = any(marcador['descricao'] == 'NFS-e Emitida' for marcador in marcadores)
                if nfse_emitida:
                    print('NFSe já emitida, pulando...')
                    continue

                print('Emitindo NFSe')
                response = incluir_nota_servico(token_tiny, pedido, percentual_iss)
                time.sleep(10)

                if response['retorno']['status'] == 3:
                    id_nota = response['retorno']['registros'][0]['registro']['id']
                    print(id_nota)
                    enviar_nota_servico(token_tiny, id_nota)
                    time.sleep(10)

                    marcadores = [{
                        "descricao": 'NFS-e Emitida'
                    }]
                    incluir_marcadores_v3(access_token, id_pedido, marcadores)
                    break
                else:
                    if response['retorno']['status'] == '2':
                        if response['retorno']['registros']['registro']['codigo_erro'] == '31':
                            marcadores = [{
                                "descricao": 'NFS-e Emitida'
                            }]
                            incluir_marcadores_v3(access_token, id_pedido, marcadores)

main()
