import socket
import threading
from tkinter import *


class Client:
    def __init__(self):
        self.create_connection()

    # start connection to server
    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                host = "10.0.0.168"
                port = 3825  # placeholder num, can be any unused port matching with server
                self.s.connect((host, port))

                break
            except:
                print("error, unable to connect")
        # chat window
        self.Window = Tk()
        self.Window.withdraw()

        # login
        self.login = Toplevel()
        # title for username screen
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # label for username screen
        self.user = Label(self.login,
                          text="Please enter a username",
                          justify=CENTER,
                          font="Helvetica 14 bold")
        self.user.place(relheight=0.15,
                        relx=0.2,
                        rely=0.7)
        # another label
        self.labelName = Label(self.login,
                               text="username: ",
                               font="Helvetica 14")
        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # type box
        self.username = Entry(self.login,
                              font="Helvetica 14")
        self.username.place(relwidth=0.4,
                            relheight=0.12,
                            relx=0.35,
                            rely=0.2)

        # focus
        self.username.focus()

        # button to continue
        self.go = Button(self.login,
                         text="continue",
                         font="Helvetica 14 bold",
                         command=lambda: self.continuing(self.username.get()))
        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()

    def continuing(self, name):
        self.login.destroy()
        self.layout(name)
        # start thread
        receiving_thread = threading.Thread(target=self.receiving, args=())
        receiving_thread.start()

    def layout(self, name):
        self.name = name
        # chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#2B2A38")
        self.label_head = Label(self.Window,
                               bg="#2B2A38",
                               fg="#D4D3E3",
                               text=self.name,
                               font="Helvetica 14 bold",
                               pady=5)

        self.label_head.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#A1A5B5")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.text_cons = Text(self.Window,
                              width=20,
                              height=2,
                              bg="#2B2A38",
                              fg="#D4D3E3",
                              font="Helvetica 14",
                              padx=5,
                              pady=5)

        self.text_cons.place(relheight=0.745,
                             relwidth=1,
                             rely=0.08)

        self.label_bottom = Label(self.Window,
                                  bg="#A1A5B5",
                                  height=80)

        self.label_bottom.place(relwidth=1,
                                rely=0.825)

        self.new_message = Entry(self.label_bottom,
                                 bg="#2C3E50",
                                 fg="#D4D3E3",
                                 font="Helvetica 14")
        self.new_message.place(relwidth=0.74,
                               relheight=0.06,
                               rely=0.008,
                               relx=0.011)

        self.new_message.focus()

        # send button
        self.button_send = Button(self.label_bottom,
                                  text="Send",
                                  font="Helvetica 14 bold",
                                  width=20,
                                  bg="#A1A5B5",
                                  command=lambda: self.send_button(self.new_message.get()))
        self.button_send.place(relx=0.77,
                               rely=0.008,
                               relheight=0.06,
                               relwidth=0.22)

        self.text_cons.config(cursor="arrow")

        # scroll bar
        scrollbar = Scrollbar(self.text_cons)

        # place the scroll bar into gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.text_cons.yview)

        self.text_cons.config(state=DISABLED)

    def receiving(self):
        while True:
            try:
                message = self.s.recv(1204).decode("utf-8")
                if message == 'NAME':
                   self.s.send(self.name.encode("utf-8"))
                else:
                    self.text_cons.config(state=NORMAL)
                    self.text_cons.insert(END, message + "\n\n")

                    self.text_cons.config(state=DISABLED)
                    self.text_cons.see(END)
            except:
                print("error")
                self.s.close()
                break

    def sending(self):
        self.text_cons.config(state=DISABLED)
        while True:
            message = f"{self.name}: {self.message}"
            self.s.send(message.encode("utf-8"))
            break
        
    def send_button(self, message):
        self.text_cons.config(state=DISABLED)
        self.message = message
        self.new_message.delete(0, END)
        sending_thread = threading.Thread(target=self.sending)
        sending_thread.start()


client = Client()
