from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import sys
import os.path
import threading


def start():

    counter = 0
    maxClients = int(sys.argv[2])

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", int(sys.argv[1])))
    serverSocket.listen()
    print("server started on port: {}".format(sys.argv[1]))

    while True:

        clientSocket, addr = serverSocket.accept()

        t1 = threading.Thread(target=client, args=(clientSocket,))
        t1.start()
        t1.join()







def client(client_soc):

    message = client_soc.recv(1024).decode()

    #parse the msg to get html
    fileName = message.split()[1]

    #if exist open and send the content to the client
    indir = os.path.isdir(fileName)

    if indir == True:
        content = open(fileName)
        text = content.read()
        client_soc.send("HTTP/1.0 200 OK:\n\n{}\r\n".format(text).encode())

    else:
        client_soc.send('HTTP/1.0 404 NOT FOUND\r\n')
        client_soc.close()
    return 0



start()



