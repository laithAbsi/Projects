import socket
import threading

# Global Variables
clients = []
client_names = {}

# Function Definitions
def broadcast(message, client_address):
    for client in clients:
        if client != client_address:
            try:
                serverSocket.sendto(message.encode(), client)
            except:
                pass

def handle_client(client_address, client_name):
    welcome_msg = f'{client_name} has joined the chat room.'
    print(welcome_msg)
    broadcast(welcome_msg, client_address)

    while True:
        try:
            message, addr = serverSocket.recvfrom(1024)
            message = message.decode()
            if not message or message == 'exit':
                break
            print(f'Received: {message} from {addr}')
            broadcast(message, client_address)
        except:
            break

    goodbye_msg = f'{client_name} has left the chat room.'
    print(goodbye_msg)
    broadcast(goodbye_msg, client_address)
    clients.remove(client_address)
    del client_names[client_address]

def run(serverSocket, serverPort):
    print(f"Server started on port {serverPort}")
    serverSocket.bind(('127.0.0.1', serverPort))
    while True:
        message, client_address = serverSocket.recvfrom(1024)
        if client_address not in clients:
            clients.append(client_address)
            client_names[client_address] = message.decode()
            threading.Thread(target=handle_client, args=(client_address, message.decode())).start()
        else:
            broadcast(message.decode(), client_address)

if __name__ == "__main__":
    serverPort = 9301
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run(serverSocket, serverPort)
