'''
Implementação do cliente
Autoras:
  NOME                    | LOGIN | GRR 
- Bianca Mendes Francisco | bmf23 | 20234263
- Nathália Nogueira Alves | nna23 | 20232349
'''

import socket
import sys
import os
import json
import datetime

def send_msg(client, data):
    json_str = json.dumps(data)
    msg = json_str.encode("utf-8")
    try:
        client.sendall(msg)
    except OSError as e:
        print(f"\033[31mErro ao enviar dados. Erro: {e}\033[0m")
        exit(1)

def receive_msg(client):
    data = client.recv(8192).decode("utf-8")
    data = json.loads(data)
    
    return data

def get_valid_menu_option():
    option = -1

    while 1: 
        print("---------- OPÇÕES ----------\n" \
              "1 - Criar conta\n" \
              "2 - Adicionar movimentação\n" \
              "3 - Verificar saldo\n" \
              "4 - Sair")
        
        option = input("Escolha uma opção: ")
        if option in ("1", "2", "3", "4"):
            return int(option)
        else:
            print("\033[31mOpção inválida.\n\033[0m")

# Recebe dados para a criação da conta e envia ao servidor
def request_account_creation(client):
    while True:
        try:
            value = int(input("\nEntre com o valor inicial: "))
            break
        except ValueError:
            print("\033[31mValor inválido.\033[0m")

    owner = input("Entre com o nome do dono da conta: ")
           
    data = {
        "option": 1,
        "value": value,
        "owner": owner 
    }

    send_msg(client, data)
    return data

# Recebe dados da transação e envia ao servidor
def request_transaction(client): 
    while True:
        type = input("\nEntre com o tipo de movimentação (s para saque ou d para depósito):")
        if type.lower() not in ('s', 'd'):
            print("\033[31mTipo inválido\033[0m")
        else:
            break

    while True:
        try:
            value = int(input("Entre com o valor da movimentação: "))
            break
        except ValueError:
            print("\033[31mValor inválido.\033[0m")

    owner = input("Entre com o nome do dono da conta: ")

    data = {
        "option": 2,
        "type": type.lower(),
        "value": value,
        "owner": owner
    }

    send_msg(client, data)
    return data

# Recebe dados da requisição de saldo e envia ao servidor
def request_balance_check(client):

    owner = input("Entre com o nome do dono da conta: ")

    data = {
       "option": 3,
        "owner": owner
    }

    send_msg(client, data)
    return data

# Pede encerramento de conexão
def request_exit(client):
    data = {
        "option": 4
    }
    send_msg(client, data)
    return data

# Função principal do cliente
def menu_loop(client):
    while (1) :
        option = get_valid_menu_option()
        if (option == 1):
            data = request_account_creation(client)
        
            response = receive_msg(client)
            if response["res"] == 0:
                print(f"\033[31m[cliente - {datetime.datetime.now()}] Enviei uma mensagem de criação de conta, mas não pôde ser realizada porque já existe conta com proprietário: {data['owner']}\n\033[0m")
            elif response["res"] == 1:
                print(f"\033[32m[cliente - {datetime.datetime.now()}] Enviei uma mensagem de criação de conta com valor inicial {data['value']} e proprietário {data['owner']}\n\033[0m")

        elif (option == 2):
            data = request_transaction(client)
            print(f"\033[32m[cliente - {datetime.datetime.now()}] Enviei uma mensagem de movimentação para a conta de {data['owner']} com valor {data['value']} e tipo {data['type']}\033[0m")
            
            response = receive_msg(client)           
            if response["res"] == -1:
                print(f"\033[31m[cliente - {datetime.datetime.now()}] A movimentação não pôde ser adicionada porque não existe conta com proprietário: {data['owner']}\n\033[0m")
            elif response["res"] == 0:
                print(f"\033[31m[cliente - {datetime.datetime.now()}] A movimentação era inválida, então não foi adicionada pelo servidor\n\033[0m")
            elif response["res"] == 1:
                print(f"\033[32m[cliente - {datetime.datetime.now()}] Movimentação validada e adicionada na blockchain pelo servidor\n\033[0m")
        
        elif (option == 3):
            data = request_balance_check(client)
            response = receive_msg(client)

            if response["res"] == 0:
                print(f"\033[31m\nO saldo não pode ser verificado porque não existe conta com proprietário: {data['owner']}.\033[0m")
            elif response["res"] == 1:
                print(f"\nO saldo da conta é {response['balance']}")
            
            print(f"\033[32m[cliente - {datetime.datetime.now()}] Recebi um retorno do pedido de verificação de saldo para a conta de {data['owner']}\n\033[0m")

        elif option == 4:
            data = request_exit(client)
            print(f"\033[31m\n[cliente - {datetime.datetime.now()}] Encerrando conexão com o servidor ('{server_host}', {server_port})\n\033[0m")
            break

# Verificação dos parâmetros
if len(sys.argv) != 3:
    print("\033[31mUso correto: python3 client.py <nome-servidor> <porta>\033[0m")
    exit(1)

# Obtêm endereço IP do servidor
try:
    server_host = sys.argv[1] # Nome do servidor
    server_ip = socket.gethostbyname(server_host)
except socket.gaierror as e:
    print(f"\033[31mFalha ao obter o endereco IP do servidor. Erro: {e}\033[0m")
    exit(1)

# Porta do servidor
server_port = int(sys.argv[2])  
    
# Cria socket do cliente
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError as e:
    print(f"\033[31mFalha ao abrir o socket. Erro: {e}\033[0m")
    exit(1)
    
# Estabelece conexão com o servidor 
try:
    client.connect((server_ip, server_port))
    print(f"\033[32m[cliente - {datetime.datetime.now()}] Conectei ao servidor ('{server_host}', {server_port})\n\033[0m")
except (socket.timeout, ConnectionRefusedError, OSError) as e:
    print(f"\033[31mFalha ao conectar ao servidor. Erro: {e}\033[0m")
    exit(1)

menu_loop(client)

# Fecha socket 
client.close()
exit(0)