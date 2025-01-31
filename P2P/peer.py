import socket
import threading

def handle_client(client_socket):
    """Function to handle messages received from a client."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
            else:
                break
        except:
            break
    client_socket.close()

def server_mode():
    """Server mode: listens for connections and creates a thread for each client."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))  # Listens on all network interfaces on port 9999
    server.listen(5)
    print("Server waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection received from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def client_mode():
    """Client mode: connects to another peer and sends messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Enter the peer IP address to connect: ")
    client_socket.connect((host, 9999))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    
    while True:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))

def receive_messages(client_socket):
    """Receives messages from a connected peer."""
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
    # Starts server mode in a separate thread
    threading.Thread(target=server_mode).start()

    # Starts client mode in the same script
    client_mode()
