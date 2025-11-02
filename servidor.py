import socket
import sys

TAMFILA = 5

def run_server():

    if len(sys.argv) != 2:
        print("Uso correto: <porta>")
        exit(1)

    try:
        server_ip = socket.gethostname()
    except OSError as e:
        print("Falha ao obter o próprio endereço IP. Erro: {e}")
        exit(1)

    port = int(sys.argv[1])

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print(f"Falha ao abrir o socket. Erro: {e}")
        exit(1)

    try:
        server.bind((server_ip, port))
    except OSError as e:
        print(f"Falha ao fazer o bind. Erro: {e}")
        exit(1)

    server.listen(TAMFILA)
    print(f"Listening on {server_ip}:{port}")

    while True:

        try: 
            client_socket, client_address = server.accept()
        except OSError as e:
            print(f"Falha ao estabelecer a conexão. Erro: {e}")

        request = client_socket.recv(8192)
        request = request.decode("utf-8") 

        print(f"Server received: {request}")

        response = request.encode("utf-8") 
        client_socket.sendall(response)

        client_socket.close()



run_server()
