import socket
import threading


class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = "10.0.0.168"
        port = 3825

        self.clients = []

        self.s.bind((host, port))
        self.s.listen(100)

        print('IP: ' + str(host))
        print('Port: ' + str(port))

        self.username_lookup = {}

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode("utf-8")

            print('New connection. Username: ' + str(username))
            self.message_all('New person joined, username: ' + username)

            self.username_lookup[c] = username

            self.clients.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def message_all(self, msg):
        for connection in self.clients:
            connection.send(msg.encode("utf-8"))

    def handle_client(self, c, addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)

                print(str(self.username_lookup[c]) + ' left...')
                self.message_all(str(self.username_lookup[c]) + ' left...')

                break

            if msg.decode("utf-8") != '':
                print('New message: ' + str(msg.decode("utf-8")))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)


server = Server()