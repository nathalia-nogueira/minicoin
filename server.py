import socket
import sys

QUEUESIZE = 5

def run_server():

    # Verificação dos parametros
    if len(sys.argv) != 2:
        print("Uso correto: <porta>")
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

    while True:

        # Espera tentativa de conexão
        try: 
            client_socket, client_address = server.accept()
        except OSError as e:
            print(f"Falha ao estabelecer a conexão. Erro: {e}")
        except KeyboardInterrupt:
            exit(0)

        # Recebe mensagem
        request = client_socket.recv(8192).decode("utf-8") 
        print(f"Server received: {request}")

        # Envia resposta 
        client_socket.sendall(request.encode("utf-8"))

        # Fecha socket criado pra conexão com o cliente
        client_socket.close()



run_server()
