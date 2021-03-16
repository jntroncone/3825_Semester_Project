import socket
import threading



class Client:
    def __init__(self):
        self.create_connection()

    # start connection to server
    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                host = "10.0.0.168"
                port = 3825 # placeholder num, can be any unused port matching with server
                self.s.connect((host, port))

                break
            except:
                print("error, unable to connect")

        self.username = input('Enter username -> ')
        self.s.send(self.username.encode("utf-8"))

        # start thread 1
        receiver = threading.Thread(target=self.receiving, args=())
        receiver.start()
        # start thread 2
        sender = threading.Thread(target=self.sending, args=())
        sender.start()

    def receiving(self):
        while True:
            print(self.s.recv(1204).decode("utf-8"))

    def sending(self):
        while True:
            self.s.send((self.username + ' -> ' + input()).encode("utf-8"))


client = Client()
