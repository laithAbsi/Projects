import socket
import argparse
import threading
import sys

def send_messages(sock, clientname):
    while True:
        try:
            message = input()
            if message:
                formatted_message = f'{clientname}> {message}'
                sock.sendall(formatted_message.encode())
                if message == 'exit':  # If the client sends 'exit', it closes its connection.
                    print('You have exited the chat room.')
                    sock.close()
                    sys.exit()
        except:
            sys.exit()

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                print('Connection closed by server.')
                sys.exit()
            print(data)
        except:
            sys.exit()

def run(clientSocket, clientname):
    clientSocket.sendall(clientname.encode())
    threading.Thread(target=send_messages, args=(clientSocket, clientname)).start()
    threading.Thread(target=receive_messages, args=(clientSocket,)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_addr, server_port))

    run(client_socket, client_name)
