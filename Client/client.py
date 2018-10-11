#from socket import AF_INET, socket, SOCK_STREAM
import socket
import datetime
from threading import Thread
from MessageHandler import *

class Client:
    BUFFER_SIZE = 2048
    PORT_SERVER = 6000
    PORT_P2P = 7000
    HOST_SERVER = '10.102.28.99'#'127.0.0.1'

    socketClient = {}

    def __init__(self, hostServer, portServer):
        self.hostServer = self.HOST_SERVER #IPv4 Address of the server
        self.portServer = self.PORT_SERVER
        self.Thread = []
    #Functions to communicate with Server#
    def sendServer(self, text):
        ret = self.socketServer.send(text.encode('utf-16'))
        if ret == 0:
            #Socket is close
            print('The socket is closed')
        else:
            print('Message sent to server correctly')

    def connectServer(self) :
        try :
            self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketServer.connect((self.hostServer, self.portServer))
        except :
            print('connection refused, the server is down!\n We apologize for the inconvenient')
            return

    def retrieveMessage(self, msgs) :
        msg = msgs.split('^/')
        for x in msg :
            block = x.split('/^')
            print('sender :' + block[0])
            print('text : ' + block[1])
            print('time : ' + block[2])

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
            if(len(msgs) > 1) :
                value = msgs[1]
            if identifier.isdigit():
                if int(identifier) > 0 :
                    print('There are messages pending in the server')
                    self.retrieveMessage(msgs[1]);
                else :
                    print('There are no messages for you')
                return 'success'
            elif identifier == '!' :
                return value
            elif identifier == '?' :
                return value
            elif identifier == '-' :
                return value
            elif identifier == '.' :
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
        if msg == 0 :
            print('Error in registration')
        else :
            print('Succesfully registered')

    def login(self, username, password):
        self.username = username
        self.sendServer('2|' + username + ',' + password)
        msg = int(self.receiveServer())
        if msg == 1 :
            print('Login done succesfully')

            self.receiveServer()

            mh = MessageHandler()
            mh.start()
        elif msg == 0 :
            print('Wrong Username or Password')
        elif msg == -1 :
            print('You are already connected with another device')
        else:
            print(msg)

    def startConnection(self, receiver):
        self.sendServer('3|' + receiver)
        value = self.receiveServer()
        msg = ''
        if value.isdigit() :
            if value == '0' :
                msg = 'user offline'
                return 0
            elif value == '-1' :
                msg = 'Error: user does not exist'
            elif value == '-2' :
                msg = 'Error: you can not connect with yourself'
        else :
            ip = value
            msg = receiver + ' has IP: ' + value
        print(msg)
        if not value.isdigit() :
            self.socketClient[receiver] = socket.socket()
            self.socketClient[receiver].connect((ip, self.PORT_P2P))
            self.socketClient[receiver].send(self.username.encode('utf-16'))
            return 1
        return -1

    def sendMessageOffline(self, receiver, text, time):
        self.sendServer('4|' + receiver + '/^' + text + '/^' + time)
        msg = self.receiveServer()
        if msg == 1:
            print('Message send correctly')
        elif msg == 0:
            print('Error in the database! Try again later!')
        print('Messaggio inviato al server e salvato sul server')

    def sendClient(self, receiver, text, event=None):  # event is passed by binders of the tkinter GUI automatically
       #Handles sending of messages
        print('Il messaggio da inviare è ' + text)
        if not receiver in self.socketClient.keys() :
            msg = self.startConnection(receiver)
            if msg == 0 : #client offline
                self.socketClient[receiver] = 'server'
            elif msg == 1 : #client online, connection established correctly
                print('Connection established with ' + receiver)
                #self.socketClient[receiver].send(text.encode('utf-16'))
        if self.socketClient[receiver] == 'server' :
            self.sendMessageOffline(receiver, text, str(datetime.datetime.now()).split('.')[0])
        else :
            self.socketClient[receiver].send(text.encode('utf-16'))

'''
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
