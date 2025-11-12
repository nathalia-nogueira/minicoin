'''
Implementação do servidor
Autoras:
  NOME                    | LOGIN | GRR 
- Bianca Mendes Francisco | bmf23 | 20234263
- Nathália Nogueira Alves | nna23 | 20232349
'''

import socket
import sys
import json
import datetime
from blockchain import Blockchain

QUEUESIZE = 5

# Envia a mensagem data ao cliente client_socket
def send_msg(client_socket, data):
    json_str = json.dumps(data)
    msg = json_str.encode("utf-8")
    try:
        client_socket.sendall(msg)
    except OSError as e:
        print(f"Erro ao enviar dados. Erro: {e}")
        exit(1)

# Recebe mensagem por client_socket e formata
def receive_msg(client_socket):
    data = client_socket.recv(8192).decode("utf-8") 
    data = json.loads(data)
    
    return data

# Lida com pedido de criação de conta
def handle_create_account(data):
    account = Blockchain(data["owner"], data["value"])
    return account

# Lida com pedido de transação
def handle_transaction(account, data):
    # Verifica se a conta existe
    if account is None:
        res = -1
    else: 
        # Verifica o tipo da transação
        if data["type"] == "s":
            res = account.addBlock(account.OP_WITHDRAWAL, data["value"])
        elif data["type"] == "d":
            res = account.addBlock(account.OP_DEPOSIT, data["value"])

    # Estrutura retorno e envia ao cliente
    data = {
        "option": 2,
        "res": res
    }
    send_msg(client_socket, data)
    
    return res        

# Lida com o pedido de verificação de saldo
def handle_balance_check(account):
    # Verifica se a conta existe
    if account is None:
        res = 0
        balance = 0
    else:
        res = 1
        balance = account.calculateBalance()
  
    # Estrutura retorno e envia ao cliente
    data = {
        "option": 3,
        "res": res,
        "balance": balance
    }
    send_msg(client_socket, data)
    
    return res, balance 

# Lida com requisições do cliente
def handle_client(client_socket):
    account = None

    while(1):
        request = receive_msg(client_socket)
        option = request["option"]

        # Opção 1: criação de conta
        if option == 1:
            if account is not None:
                res = 0
                print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido de criação de conta. Não será realizado porque já existe conta\n")
            else:
                res = 1
                account = handle_create_account(request)
                print(f"\n[servidor - {datetime.datetime.now()}] Iniciei uma conta com dono {account.head.owner} e valor inicial {account.calculateBalance()}\n")

            data = {
                "option": 1,
                "res": res 
            }
            send_msg(client_socket, data)

        # Opção 2: adição de movimentação
        elif option == 2:
            res = handle_transaction(account, request)
            
            if res == -1:
                print(f"\n[servidor - {datetime.datetime.now()}] A movimentação {request['type']} com valor {request['value']} não pôde ser adicionada porque não existe conta\n")
            elif res == 0:
                print(f"\n[servidor - {datetime.datetime.now()}] A movimentação {request['type']} com valor {request['value']} não pôde ser adicionada porque é inválida\n")
            elif res == 1:
                print(f"\n[servidor - {datetime.datetime.now()}] Adicionei a movimentação {request['type']} com valor {request['value']}\n")
        
        # Opção 3: verificação de saldo
        elif option == 3:
            print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido de verificação de saldo")
            res, balance = handle_balance_check(account)

            if res == 0:
                print(f"[servidor - {datetime.datetime.now()}] Não enviei retorno de saldo porque não existe conta\n")
            elif res == 1:
                print(f"[servidor - {datetime.datetime.now()}] Enviei um retorno com saldo = {balance}\n")

        # Opção 4: encerrar
        elif option == 4:
            print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido para fechar comunicação.\n")
            break

# Verificação dos parametros
if len(sys.argv) != 2:
    print("Uso correto: python server.py <porta>")
    exit(1)

# Obtêm seu próprio endereço IP 
try:
    server_ip = socket.gethostname()
except OSError as e:
    print("Falha ao obter o próprio endereço IP. Erro: {e}")
    exit(1)

# Porta do servidor
server_port = int(sys.argv[1])

# Cria socket do servidor
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError as e:
    print(f"Falha ao abrir o socket. Erro: {e}")
    exit(1)

# Realiza bind do servidor
try:
    server.bind((server_ip, server_port))
except OSError as e:
    print(f"Falha ao fazer o bind. Erro: {e}")
    exit(1)

# Coloca servidor em modo escuta
server.listen(QUEUESIZE)
print(f"Listening on {server_ip}:{server_port}")

while 1:
    # Espera tentativa de conexão
    try: 
        client_socket, client_address = server.accept()
        print(f"[servidor - {datetime.datetime.now()}] Conectei ao cliente {client_address}\n")

    except OSError as e:
        print(f"Falha ao estabelecer a conexão. Erro: {e}")
    except KeyboardInterrupt:
        exit(0)
    
    handle_client(client_socket)
    print(f"[servidor - {datetime.datetime.now()}] Encerrei conexão com o cliente {client_address}\n")
    
    # Fecha socket criado pra conexão com o cliente
    client_socket.close()