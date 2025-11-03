import socket
import sys

def run_client():

    # Verificação dos parâmetros
    if len(sys.argv) != 4:
        print("Uso correto: <nome-servidor> <porta> <dados>")
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

    # Codifica mensagem recebida como parâmetro
    msg = sys.argv[3].encode("utf-8")

    # Envia mensagem
    try:
        client.sendall(msg)
    except OSError as e:
        print(f"Erro ao enviar dados. Erro: {e}")
        exit(1)

    # Resposta do servidor
    response = client.recv(8192).decode("utf-8")
    print(f"Client received: {response}")

    # Fecha socket 
    client.close()
    exit(0)



run_client()
