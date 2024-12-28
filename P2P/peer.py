import socket
import threading

def handle_client(client_socket):
    """Função para lidar com mensagens recebidas de um cliente."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Recebido: {message}")
            else:
                break
        except:
            break
    client_socket.close()

def server_mode():
    """Modo servidor: escuta conexões e cria uma thread para cada cliente."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))  # Escuta em todas as interfaces de rede na porta 9999
    server.listen(5)
    print("Servidor esperando por conexões...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão recebida de {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def client_mode():
    """Modo cliente: conecta a outro peer e envia mensagens."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Digite o endereço IP do peer para conectar: ")
    client_socket.connect((host, 9999))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    
    while True:
        message = input("Você: ")
        client_socket.send(message.encode('utf-8'))

def receive_messages(client_socket):
    """Recebe mensagens de outro peer conectado."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Peer: {message}")
            else:
                break
        except:
            break

if __name__ == "__main__":
    # Inicia o modo servidor em uma thread separada
    threading.Thread(target=server_mode).start()

    # Inicia o modo cliente no mesmo script
    client_mode()
