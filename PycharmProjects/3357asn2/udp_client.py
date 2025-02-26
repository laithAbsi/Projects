import socket
import argparse
import threading

# Global Variables
exit_flag = False

# Function Definitions
def send_messages(clientSocket, clientname, serverAddr, serverPort):
    global exit_flag
    while True:
        try:
            message = input()
            if message:
                formatted_message = f'{clientname}> {message}'
                clientSocket.sendto(formatted_message.encode(), (serverAddr, serverPort))
                if message == 'exit':
                    exit_flag = True
                    break
        except:
            print('An error occurred while sending your message.')

def receive_messages(clientSocket, clientname, serverAddr, serverPort):
    global exit_flag
    while True:
        if exit_flag:
            break
        try:
            data, addr = clientSocket.recvfrom(1024)
            print(data.decode())
        except:
            print('An error occurred while receiving a message.')

def run(clientSocket, clientname, serverAddr, serverPort):
    clientSocket.sendto(clientname.encode(), (serverAddr, serverPort))
    threading.Thread(target=send_messages, args=(clientSocket, clientname, serverAddr, serverPort)).start()
    threading.Thread(target=receive_messages, args=(clientSocket, clientname, serverAddr, serverPort)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run(clientSocket, clientname, serverAddr, serverPort)
