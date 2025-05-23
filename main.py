import os
import time
import logging
from dotenv import load_dotenv
import datetime
from api_tiny_v3 import get_orders_v3, get_markers_v3, add_markers_v3
from api_miliapp import get_tiny_tokens
from api_tiny_v2 import add_service_invoice, send_service_invoice
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Configure logging
logging.basicConfig(
    filename='process_orders.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
TOKEN_TINY_CWB = os.getenv('TOKEN_TINY_CWB')
TOKEN_TINY_FOR = os.getenv('TOKEN_TINY_FOR')


def process_orders(start_date):
    os.system('cls')
    origins = ['miligrama', 'miligrama_nordeste']

    for origin in origins:
        if origin == 'miligrama':
            access_token, refresh_token = get_tiny_tokens(origin)
            token_tiny = TOKEN_TINY_CWB
            iss_percentage = '5'
        elif origin == 'miligrama_nordeste':
            access_token, refresh_token = get_tiny_tokens(origin)
            token_tiny = TOKEN_TINY_FOR
            iss_percentage = '3'

        logging.info('Fetching order list')
        print('Fetching order list')
        search_params = {
            'orderBy': 'asc',
            'dataInicial': start_date,
        }
        order_list = get_orders_v3(access_token, search_params)

        k = 0
        for order in order_list:
            k += 1
            logging.info(f'===== origin: {origin} => {k} / {len(order_list)} =====')
            print(f'===== origin: {origin} => {k} / {len(order_list)} =====')
            logging.info(order['numeroPedido'])
            print(order['numeroPedido'])
            
            order_id = order['id']
            status = order['situacao']
            if status == 8 or status == 0 or status == 2:
                logging.info('Order not approved, skipping...')
                print('Order not approved, skipping...')
                continue
            else:
                logging.info('Fetching markers')
                print('Fetching markers')
                while True:
                    try:
                        markers = get_markers_v3(access_token, order_id)
                        logging.info(markers)
                        print(markers)
                        break
                    except:
                        logging.error('Error fetching markers')
                        print('Error fetching markers')
                        time.sleep(2)

                nfse_issued = any(marker['descricao'] == 'NFS-e Emitida' for marker in markers)
                if nfse_issued:
                    logging.info('NFSe already issued, skipping...')
                    print('NFSe already issued, skipping...')
                    continue

                while True:
                    try:
                        logging.info('Issuing NFSe')
                        print('Issuing NFSe')
                        logging.info(f'iss_percentage: {iss_percentage}')
                        print(f'iss_percentage: {iss_percentage}')

                        response = add_service_invoice(token_tiny, order, iss_percentage)
                        logging.info(response)
                        print(response)
                        time.sleep(10)
                        if response['retorno']['status_processamento'] != 1 and response['retorno']['status_processamento'] != '1':
                            break
                        else:
                            if response['retorno']['codigo_erro'] == '3':
                                print(response['retorno']['erros'][0]['erro'])
                                logging.info(response['retorno']['erros'][0]['erro'])
                                print(order)
                                logging.info(order)
                                break
                    except Exception as e:
                        logging.error(f'Error issuing NFSe: {e}')
                        print(f'Error issuing NFSe: {e}')
                        time.sleep(2)

                if response['retorno']['status_processamento'] == 3 or response['retorno']['status_processamento'] == '3':
                    print('Sending NFSe')
                    logging.info('Sending NFSe')
                    invoice_id = response['retorno']['registros'][0]['registro']['id']
                    logging.info(f'invoice_id: {invoice_id}')
                    print(f'invoice_id: {invoice_id}')
                    send_service_invoice(token_tiny, invoice_id)
                    time.sleep(10)

                    while True:
                        try:
                            logging.info('Adding markers')
                            print('Adding markers')
                            markers = [{
                                "descricao": 'NFS-e Emitida'
                            }]
                            response = add_markers_v3(access_token, order_id, markers)
                            logging.info(response)
                            print(response)
                            if response.status_code == 204:
                                break
                        except:
                            logging.error('Error adding markers')
                            print('Error adding markers')
                            time.sleep(2)
                else:
                    if response['retorno']['status_processamento'] == 2 or response['retorno']['status_processamento'] == '2':
                        print(response['retorno']['registros']['registro'])
                        if response['retorno']['registros']['registro']['codigo_erro'] == '31':
                            logging.info('Service already issued')
                            print('Service already issued')
                            while True:
                                try:
                                    logging.info('Adding markers')
                                    print('Adding markers')
                                    markers = [{
                                        "descricao": 'NFS-e Emitida'
                                    }]
                                    response = add_markers_v3(access_token, order_id, markers)
                                    logging.info(response)
                                    print(response)
                                    if response.status_code == 204:
                                        break
                                except:
                                    logging.error('Error adding markers')
                                    print('Error adding markers')
                                    time.sleep(2)


def execute_process_orders(start_date):
    try:
        process_orders(start_date)
        messagebox.showinfo("Success", "The process_orders function executed successfully!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


def create_gui():
    root = tk.Tk()
    root.title("Emissor de NFS-e")

    # Label and Date Selector
    label_start_date = tk.Label(root, text="Start Date:")
    label_start_date.grid(row=0, column=0, padx=10, pady=10)

    start_date_entry = ttk.Entry(root)
    start_date_entry.insert(0, "2025-05-21")  # Default placeholder value
    start_date_entry.grid(row=0, column=1, padx=10, pady=10)

    # Run Button
    btn_run = tk.Button(root, text="Run", command=lambda: execute_process_orders(start_date_entry.get()))
    btn_run.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()