from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Client:

    def __init__(self, hostServer, portServer, bufferSize):
        self.hostServer = hostServer; #IPv4 Address of the server
        self.portServer = 1745
        self.BUFFER_SIZE = 2000

    #Functions to communicate with Server#

    def connectServer(self):
        self.connectionToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((host, port))

    def sendServer(self, ...):

    ######################################

    #Functions for the FrontEnd#

    def register(self, ...):

    def login(self, ...):

    def sendMessage(self, ...):

    ############################

    #Functions to communicate with others Clients

    #UDP connection with clients?
    def connectClient(self, ...):

    def receiveMessage(self, ...):
        while True:
            try:
                msg = sockerRicezione.recv(self.BUFFER_SIZE).decode("utf8")
                #insert into a list of the front end (tkinter.Listbox) @Amedeo
                ...
            except OSError: #The other client could have left the chat
                #the Thread that listens can put to do something else or closed
                break

    def send(self, event=None, ...):  # event is passed by binders of the tkinter GUI automatically
        #Handles sending of messages
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        if(self.clientReceiverOnline(index))
            client_socket.send(bytes(msg, "utf8"))
        else
            server_socket.send(bytes(msg, "utf8"))
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
