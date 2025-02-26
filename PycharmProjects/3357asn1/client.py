import socket
import sys


port = int(sys.argv[1])
filename = sys.argv[2]
IP = "127.0.0.1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the server
client.connect((IP, port))


def send(message):

    message = message.encode('utf-8')

    client.send(message)
    print(client.recv(2048).decode('utf-8'))
    print(client.recv(2048).decode('utf-8'))
    content = client.recv(2048).decode('utf-8')
    print(content)
    client.close()


try:
    # Send get request for filename
    send(f"GET /{filename} HTTP/1.1\r\nHost: {IP}\r\n\r\n")
except ConnectionResetError:
    print("Cannot Connect to the Server with IP: {}".format(IP))





