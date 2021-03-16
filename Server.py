import socket
import threading


class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = "10.0.0.168"
        port = 3825

        self.usernames = []
        self.clients = []
        self.s.bind((host, port))
        self.s.listen()
        print('listening at...')
        print('IP: ' + str(host))
        print('Port: ' + str(port))


        while True:
            c, addr = self.s.accept()
            c.send("NAME".encode("utf-8"))
            username = c.recv(1024).decode("utf-8")

            print('New connection. Username: ' + str(username))
            self.message_all(f"{username} has joined, welcome!")

            self.usernames.append(username)

            self.clients.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

            self.message_all(f"Currently {threading.activeCount()-1} active users:\n")

            for user in self.usernames:
                self.message_all(f"{user} \n")

    def message_all(self, message):
        for connection in self.clients:
            connection.send(message.encode("utf-8"))

    def handle_client(self, c, addr):
        while True:
            try:
                message = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)

                print(str(self.usernames[c]) + ' left...')
                self.message_all(str(self.usernames[c]) + ' left...')

                self.clients.remove(c)
                self.usernames.remove(c)
                break

            if message.decode("utf-8") != '':
                print(str(message.decode("utf-8")))
                for connection in self.clients:
                    # if connection != c:
                    connection.send(message)


server = Server()