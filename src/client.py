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
        print(f"Erro ao enviar dados. Erro: {e}")
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
            print("Opção inválida.")

def request_account_creation(client):
    try:
        value = int(input("\nEntre com o valor inicial: "))
    except ValueError:
        print("Valor inválido.")
        exit(1)

    owner = input("Entre com o nome do dono da conta: ")
           
    data = {
        "option": 1,
        "value": value,
        "owner": owner 
    }

    send_msg(client, data)
    return data

def request_transaction(client): 
    type = input("\nEntre com o tipo de movimentação (s para saque ou d para depósito):")
    if type.lower() not in ('s', 'd'):
        print("Tipo inválido")
        exit(1) 

    try:
        value = int(input("Entre com o valor da movimentação: "))
    except ValueError:
        print("Valor inválido.")
        exit(1)
            
    data = {
        "option": 2,
        "type": type.lower(),
        "value": value 
    }

    send_msg(client, data)
    return data

def request_balance_check(client):
    data = {
       "option": 3
    }
    send_msg(client, data)
    return data

def request_exit(client):
    data = {
        "option": 4
    }
    send_msg(client, data)
    return data

def menu_loop(client):
    while (1) :
        option = get_valid_menu_option()
        if (option == 1):
            data = request_account_creation(client)
        
            response = receive_msg(client)
            if response["res"] == 0:
                print(f"[cliente - {datetime.datetime.now()}] Enviei uma mensagem de criação de conta, mas não pôde ser realizada porque já existe conta\n")
            elif response["res"] == 1:
                print(f"[cliente - {datetime.datetime.now()}] Enviei uma mensagem de criação de conta com valor inicial {data['value']} e dono {data['owner']}\n")

        elif (option == 2):
            data = request_transaction(client)
            print(f"[cliente - {datetime.datetime.now()}] Enviei uma mensagem de movimentação de conta com valor {data['value']} e tipo {data['type']}")
            
            response = receive_msg(client)           
            if response["res"] == -1:
                print(f"[cliente - {datetime.datetime.now()}] A movimentação não pôde ser adicionada porque não existe conta\n")
            elif response["res"] == 0:
                print(f"[cliente - {datetime.datetime.now()}] A movimentação era inválida, então não foi adicionada pelo servidor\n")
            elif response["res"] == 1:
                print(f"[cliente - {datetime.datetime.now()}] Movimentação validada e adicionada na blockchain pelo servidor\n")
        
        elif (option == 3):
            data = request_balance_check(client)
            response = receive_msg(client)

            if response["res"] == 0:
                print(f"\nO saldo não pode ser verificado porque não existe conta.")
            elif response["res"] == 1:
                print(f"\nO saldo da conta é {response['balance']}")
            
            print(f"[cliente - {datetime.datetime.now()}] Recebi um retorno do pedido de verificação de saldo\n")

        elif option == 4:
            data = request_exit(client)
            break

# Verificação dos parâmetros
if len(sys.argv) != 3:
    print("Uso correto: python client.py <nome-servidor> <porta>")
    exit(1)

# Obtêm endereço IP do servidor
try:
    server_host = sys.argv[1] # Nome do servidor
    server_ip = socket.gethostbyname(server_host)
except socket.gaierror as e:
    print(f"Falha ao obter o endereco IP do servidor. Erro: {e}")
    exit(1)

# Porta do servidor
server_port = int(sys.argv[2])  
    
# Cria socket do cliente
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError as e:
    print(f"Falha ao abrir o socket. Erro: {e}")
    exit(1)
    
# Estabelece conexão com o servidor 
try:
    client.connect((server_ip, server_port))
except (socket.timeout, ConnectionRefusedError, OSError) as e:
    print(f"Falha ao conectar ao servidor. Erro: {e}")
    exit(1)

menu_loop(client)

# Fecha socket 
client.close()
exit(0)