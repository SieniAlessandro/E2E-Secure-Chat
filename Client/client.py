#from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread

class Client:
    BUFFER_SIZE = 2048
    PORT_P2P = 7000
    PORT_SERVER = 6000
    HOST_SERVER = '10.102.8.250'

    socketClient = {}

    def __init__(self, hostServer, portServer):
        self.hostServer = HOST_SERVER #IPv4 Address of the server
        self.portServer = PORT_SERVER

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
        except:
            print('connection refused, the server is down!\ We apologize for the inconvenient')
            return

    def receiveServer(self):
        ret = self.socketServer.recv(self.BUFFER_SIZE)
        if not ret:
            print('Socket closed')
            return -1
        else:
            print('Message received from Server')
            msg = ret.decode('utf-16')
            msgs = msg.split('|')
            identifier = msgs[0]
            value = msgs[1]
            if identifier.isdigit():
                if identifier > 0 :
                    #retrieveMessage(msgs[1]);
                    print('message pending in the server')
                else :
                    print('no message for you')
            elif identifier == '!' :
                return value
            elif identifier == '?' :
                return value
            else :
                return identifier


    ######################################

    #Functions for the FrontEnd#

    def register(self, username, password, name, surname, email, key):
        self.sendServer('1|' + username + ',' + password + ',' + name + ',' +
                surname + ',' + email + ',' + key)
        msg = self.receiveServer();
        print(msg)

    def login(self, username, password):
        self.sendServer('2|' + username + ',' + password)
        ret = self.receiveServer()
        if ret == 1 :
            print('Login done succesfully')
        elif ret == 0 :
            print('Wrong Username or Password')
        elif ret == -1 :
            print('You are already connected with another device')


    def startConnection(self, receiver):
        self.sendServer('3|' + receiver)
        msg = self.receiveServer(socket.AF_INET, socket.SOCK_STREAM)
        if value.isdigit() :
            if value == 0 :
                msg = 'client offline'
            elif value == -1 :
                msg = 'Error: client offline'
            elif value == -2 :
                msg = 'Error: you can not connect with yourself'
        else :
            msg = receiver + 'has IP: ' + value
        print(msg)
        if not value.isdigit() :
            self.socketClient[receiver] = socket.socket()
            self.socketClient[receiver].connect((msg, self.PORT_P2P))

    def sendMessageOffline(self, receiver, text, time):
        self.sendServer('4|' + receiver + ',' + text + ',' + time)
        msg = self.receiveServer()
        print(msg)
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
'''
