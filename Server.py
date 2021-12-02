import socket
import threading

HOST = "10.0.0.168"
PORT = 3825
FORMAT = "utf-8"

class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usernames = []
        self.clients = []
        self.s.bind((HOST, PORT))
        self.s.listen()
        print('listening at...')
        print('IP: ' + str(HOST))
        print('PORT: ' + str(PORT))

        while True:
            c, addr = self.s.accept()
            c.send("NAME".encode(FORMAT))
            username = (str(c.recv(1024).decode(FORMAT)))

            # new connection notice to all
            print('New connection. Username: ' + username)
            self.usernames.append(username)
            self.clients.append(c)
            self.message_all(f"{username} has joined, welcome!".encode(FORMAT))

            threading.Thread(target=self.handle_client, args=(c, addr)).start()

            self.message_all(f"Currently {threading.activeCount()-1} active users:\n".encode(FORMAT))
            self.display_open_connections()

            for client in self.clients:
                print(client)

    def handle_client(self, c, addr):
        while True:
            try:
                message = c.recv(1024)
            except:
                # connection closed, remove from lists and provide updated list
                c.close()
                for client in self.clients:
                    if c == client:
                        i = self.clients.index(client)

                        self.clients.pop(i)
                        self.usernames.pop(i)

                self.message_all("Someone left, here are the remaining users:".encode(FORMAT))
                self.display_open_connections()
                break
            if message.decode(FORMAT) != '':
                print(str(message.decode(FORMAT)))
                self.message_all(message)

    def message_all(self, message):
        for connection in self.clients:
            connection.send(message)

    def display_open_connections(self):
        # send current active user list to all users
        for user in self.usernames:
            self.message_all(f"{user} \n".encode(FORMAT))
            print(user)


server = Server()
