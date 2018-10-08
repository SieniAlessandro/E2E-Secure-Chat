#from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread

class Client:
    BUFFER_SIZE = 2048

    def __init__(self, hostServer, portServer):
        self.hostServer = hostServer; #IPv4 Address of the server
        self.portServer = portServer

    #Functions to communicate with Server#
    def sendServer(self, text):
        ret = self.socketServer.send(text.encode('utf-16'))
        if ret == 0:
            #Socket is close
            print('The socket is closed')
        else:
            print('Message sent to server correctly')

    def connectServer(self):
        try:
            self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketServer.connect((self.hostServer, self.portServer))
        except ConnectionRefusedError or OSError:
            print('connection refused, the server is down!\ We apologize for the inconvenient')
            return

    def receiveServer(self):
        ret = self.socketServer.recv(BUFFER_SIZE)
        if not ret:
            print('Socket closed')
        else:
            print('Message received from Server')
            return ret.decode()


    ######################################

    #Functions for the FrontEnd#

    def register(self, username, password, name, surname, email, key):
        self.sendServer('1|' + username ',' + password + ',' + name + ',' +
                surname + ',' + email + ',' + key')
        msg = self.receiveServer();

    def login(self, username, password):
        self.sendServer('2|' + username + ',' + password)
        msg = self.receiveServer();

    def sendMessage(self, receiver, text, time):
        self.sendServer('3|' + receiver + ',' + text + ',' + time)
        msg = self.receiveServer();

    '''
    ############################

    #Functions to communicate with others Clients

    #TCP connection with clients?
    def connectClient(self):
        #request to Server for the IP of the receiver
        sendServer( )

        msg = receiveServer( )

        if(check_msg_is_VALID_IP)
            #start a new connection with another client with a Thread
        else
            #with a new Thread send message to the server crypthed with key of B

    def receiveMessage(self,  ):
        while True:
            try:
                msg = sockerRicezione.recv(self.BUFFER_SIZE).decode("utf8")
                #insert into a list of the front end (tkinter.Listbox) @Amedeo

            except OSError: #The other client could have left the chat
                #the Thread that listens can put to do something else or closed
                break

    def send(self, event=None,  ):  # event is passed by binders of the tkinter GUI automatically
        #Handles sending of messages
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        if(self.clientReceiverOnline(index))
            #client_socket.send(bytes(msg, "utf8"))
        else
            self.serverSocket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            top.quit()

    def onClosing(event=None): #clean up before close
        #close the socket connection
        my_msg.set("{quit}")
        send()

    #Functions for the Security#
    ##TO DO TO DO  TO DO TO DO##
    ############################
