import socket
import sys

def run_client():

    if len(sys.argv) != 4:
        print("Uso correto: <nome-servidor> <porta> <dados>")
        exit(1)

    try:
        host = sys.argv[1]
        server_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        print(f"Falha ao obter o endereco IP do servidor. Erro: {e}")
        exit(1)

    server_port = int(sys.argv[2])  
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print(f"Falha ao abrir o socket. Erro: {e}")
        exit(1)
    
    try:
        client.connect((server_ip, server_port))
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"Falha ao conectar ao servidor. Erro: {e}")
        exit(1)

    msg = sys.argv[3].encode("utf-8")

    try:
        client.sendall(msg)
    except OSError as e:
        print(f"Erro ao enviar dados. Erro: {e}")
        exit(1)

    response = client.recv(8192)
    response = response.decode("utf-8")
    print(f"Client received: {response}")

    client.close()
    exit(0)



run_client()
