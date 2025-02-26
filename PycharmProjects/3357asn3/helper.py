import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.server = "10.11.250.207"
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            # return self.client.recv(2048).decode()
        except:
            print("Unable to connect to server")

    def send(self, data, receive=False):
        try:
            self.client.send(str.encode(data))
            if receive:
                return pickle.loads(self.client.recv(2048))  # Use pickle.loads here
            else:
                return None
        except socket.error as e:
            print(e)

    def recv(self):
        # receive with timeout
        try:
            return self.client.recv(2048).decode()
        except socket.timeout as e:
            return None