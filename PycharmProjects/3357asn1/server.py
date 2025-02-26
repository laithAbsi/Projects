
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import sys
import threading


port = int(sys.argv[1])
maxClients = int(sys.argv[2])

# address is a tuple of our serverSocket and the port serverSocket is running off on.
address = ('', port)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(address)

currentConnection = 1

# Function to handle new connections
def begin():


    serverSocket.listen()
    while True:

        # New connection accepted.
        clientSocket, address = serverSocket.accept()

        # threading out to "handle_client".
        thread1 = threading.Thread(target=client, args=(clientSocket, ))


        # Closing connection if active connections over maxClients
        if currentConnection == maxClients + 1:
            print("Client trying to connect.")
            print("Max Client Capacity Reached. Can't connect client to server")

            clientSocket.send("Max Client Capacity Reached. Can't connect client to server".encode("utf-8"))
            clientSocket.close()

            continue

        print("New connection: {} connected".format(address))

        print("Active connections: {}".format(currentConnection))

        thread1.start()


# Function to handle connections between client and the server
def client(connection):
    global currentConnection
    currentConnection += 1
    try:
        message = connection.recv(1024).decode()
        chunks = message.split(" ")
        filename = chunks[1][1:]

        content = open(filename)
        print(filename, "found")

        connection.send("HTTP/1.0 200 OK\r\n".encode("utf-8"))
        connection.send("Content-Type: text/html\r\n".encode("utf-8"))
        connection.send(message.encode("utf-8"))
        data = content.read()
        connection.send(data.encode("utf-8"))
        connection.send("\r\n".encode("utf-8"))

        connection.close()
        print("{} delivered".format(filename))

    except IOError:
        print("{} NOT found".format(filename))
        connection.send('HTTP/1.0 404 NOT FOUND\r\n'.encode("utf-8"))
        connection.close()
        print("file not found message sent to client")


print("Server is listening on port {}".format(port))
begin()
