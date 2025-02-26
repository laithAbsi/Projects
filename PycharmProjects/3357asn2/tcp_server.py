import socket
import threading

clients = []
client_names = {}

def handle_client(client_socket):
    client_name = client_socket.recv(1024).decode()
    client_names[client_socket] = client_name
    welcome_msg = f'{client_name} has joined the chat room.'
    print(welcome_msg)
    broadcast(welcome_msg, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message or message.split('>')[1].strip() == 'exit':  # Check for exit command.
                break
            print(f'Received: {message}')
            broadcast(message, client_socket)
        except:
            break

    goodbye_msg = f'{client_name} has left the chat room.'
    print(goodbye_msg)
    broadcast(goodbye_msg, client_socket)
    clients.remove(client_socket)
    del client_names[client_socket]
    client_socket.close()

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                pass

def run(serverSocket, serverPort):
    print(f"Server started on port {serverPort}")
    while True:
        client_socket, addr = serverSocket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(3)
    run(server_socket, server_port)
