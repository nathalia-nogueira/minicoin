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
account = []

# Envia a mensagem data ao cliente client_socket
def send_msg(client_socket, data):
    json_str = json.dumps(data)
    msg = json_str.encode("utf-8")
    try:
        client_socket.sendall(msg)
    except OSError as e:
        print(f"\033[31mErro ao enviar dados. Erro: {e}\033[0m")
        exit(1)

# Recebe mensagem por client_socket e formata
def receive_msg(client_socket):
    data = client_socket.recv(8192).decode("utf-8") 
    data = json.loads(data)
    
    return data

# verifica a existência da conta com proprietário == owner
def verify_account(owner, account_list):
    for i, acc in enumerate(account_list):
        if acc.head.owner == owner:
            return i  
    
    return -1

# Lida com pedido de criação de conta
def handle_create_account(data):
    tmp = Blockchain(data["owner"], data["value"])
    return tmp

# Lida com pedido de transação
def handle_transaction(data):
    # Verifica se a conta existe
    id = verify_account(data["owner"], account)
    if id == -1:
        res = -1
    else: 
        # Verifica o tipo da transação
        if data["type"] == "s":
            res = account[id].addBlock(account[id].OP_WITHDRAWAL, data["value"])
        elif data["type"] == "d":
            res = account[id].addBlock(account[id].OP_DEPOSIT, data["value"])

    # Estrutura retorno e envia ao cliente
    data = {
        "option": 2,
        "res": res
    }
    send_msg(client_socket, data)
    
    return res        

# Lida com o pedido de verificação de saldo
def handle_balance_check(request):
    # Verifica se a conta existe
    id = verify_account(request["owner"], account)
    if id == -1:
        res = 0
        balance = 0
    else:
        res = 1
        balance = account[id].calculateBalance()
  
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
    global account

    while(1):
        request = receive_msg(client_socket)
        option = request["option"]

        # Opção 1: criação de conta
        if option == 1:
            id = verify_account(request["owner"], account)
            if id != -1:
                res = 0
                print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido de criação de conta. Não será realizado porque já existe conta com proprietário: {request['owner']}\n")
            else:
                res = 1
                account.append(handle_create_account(request))
                print(f"\n[servidor - {datetime.datetime.now()}] Iniciei uma conta com dono {account[len(account)-1].head.owner} e valor inicial {account[len(account)-1].calculateBalance()}\n")

            data = {
                "option": 1,
                "res": res 
            }
            send_msg(client_socket, data)

        # Opção 2: adição de movimentação
        elif option == 2:
            res = handle_transaction(request)
            
            if res == -1:
                print(f"\n[servidor - {datetime.datetime.now()}] A movimentação {request['type']} com valor {request['value']} não pôde ser adicionada porque não existe conta com proprietário: {request['owner']}\n")
            if res == 0:
                print(f"[servidor - {datetime.datetime.now()}] A movimentação {request['type']} com valor {request['value']} não pôde ser adicionada porque é inválida\n")
            elif res == 1:
                print(f"\n[servidor - {datetime.datetime.now()}] Adicionei a movimentação {request['type']} com valor {request['value']} à conta de {request['owner']}\n")
        
        # Opção 3: verificação de saldo
        elif option == 3:
            print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido de verificação de saldo para a conta de {request['owner']}")
            res, balance = handle_balance_check(request)

            if res == 0:
                print(f"[servidor - {datetime.datetime.now()}] Não enviei retorno de saldo porque não existe conta com proprietário: {request['owner']}\n")
            elif res == 1:
                print(f"[servidor - {datetime.datetime.now()}] Enviei um retorno com saldo = {balance}\n")

        # Opção 4: encerrar
        elif option == 4:
            print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido para fechar comunicação.\n")
            break

# Verificação dos parametros
if len(sys.argv) != 2:
    print("\033[31mUso correto: python server.py <porta>\033[0m")
    exit(1)

# Obtêm seu próprio endereço IP 
try:
    server_ip = socket.gethostname()
except OSError as e:
    print("\033[31mFalha ao obter o próprio endereço IP. Erro: {e}\033[0m")
    exit(1)

# Porta do servidor
server_port = int(sys.argv[1])

# Cria socket do servidor
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError as e:
    print(f"\033[31mFalha ao abrir o socket. Erro: {e}\033[0m")
    exit(1)

# Realiza bind do servidor
try:
    server.bind((server_ip, server_port))
except OSError as e:
    print(f"\033[31mFalha ao fazer o bind. Erro: {e}\033[0m")
    exit(1)

# Coloca servidor em modo escuta
server.listen(QUEUESIZE)
print(f"\033[35mListening on {server_ip}:{server_port}\033[0m")

while 1:
    # Espera tentativa de conexão
    try: 
        client_socket, client_address = server.accept()
        print(f"\033[32m[servidor - {datetime.datetime.now()}] Conectei ao cliente {client_address}\n\033[0m")

    except OSError as e:
        print(f"\033[31mFalha ao estabelecer a conexão. Erro: {e}\033[0m")
    except KeyboardInterrupt:
        exit(0)
    
    handle_client(client_socket)
    print(f"\033[31m[servidor - {datetime.datetime.now()}] Encerrei conexão com o cliente {client_address}\n\033[0m")
    
    # Fecha socket criado pra conexão com o cliente
    client_socket.close()