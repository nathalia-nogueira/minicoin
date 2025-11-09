import socket
import sys
import json
import datetime
from blockchain import Blockchain

QUEUESIZE = 5

def send_msg(client_socket, data):
    json_str = json.dumps(data)
    msg = json_str.encode("utf-8")
    try:
        client_socket.sendall(msg)
    except OSError as e:
        print(f"Erro ao enviar dados. Erro: {e}")
        exit(1)

def handle_create_account(data):
    account = Blockchain(data["owner"], data["value"])
    return account

def handle_transaction(account, data):
    if data["type"] == "s":
        account.addBlock(account.OP_WITHDRAWAL, data["value"])
    elif data["type"] == "d":
        account.addBlock(account.OP_DEPOSIT, data["value"])

def handle_balance_check(account):
    balance = account.calculateBalance()
    data = {
        "option": 3,
        "balance": balance
    }
    send_msg(client_socket, data)  
    return balance 

def handle_client():
    account = None

    while(1):
        # Recebe mensagem
        request = client_socket.recv(8192).decode("utf-8") 
        data = json.loads(request)
            
        option = data["option"]
        if option == 1:
            account = handle_create_account(data)
            print(f"\n[servidor - {datetime.datetime.now()}] Iniciei uma conta com dono {account.head.owner} e valor inicial {account.calculateBalance()}\n")

        elif option == 2:
            handle_transaction(account, data)
            print(f"\n[servidor - {datetime.datetime.now()}] Adicionei a movimentação {data["type"]} com valor {data["value"]}\n")

        elif option == 3:
            print(f"\n[servidor - {datetime.datetime.now()}] Recebi um pedido de verificação de saldo")
            balance = handle_balance_check(account)
            print(f"[servidor - {datetime.datetime.now()}] Enviei um retorno com saldo = {balance}\n")

        elif option == 4:
            print("Recebi um pedido pra fechar o server")
            break

# Verificação dos parametros
if len(sys.argv) != 2:
    print("Uso correto: python server.py <porta>")
    exit(1)

# Obtêm seu próprio endereço IP 
try:
    server_ip = ssocket.gethostname()
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
    except OSError as e:
        print(f"Falha ao estabelecer a conexão. Erro: {e}")
    except KeyboardInterrupt:
        exit(0)
    
    handle_client()

    # Fecha socket criado pra conexão com o cliente
    client_socket.close()