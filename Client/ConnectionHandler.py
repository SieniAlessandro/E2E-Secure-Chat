import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *


class ConnectionHandler(Thread) :
    MSG_LEN = 2048
    #Constructor
    '''
        Create a new socket and bind it to the port destinated for connectio p2p
    '''
    def __init__(self, portp2p, Log, Chat, Code, Message) :
        Thread.__init__(self)
        self.ip = "0.0.0.0"
        self.portp2p = portp2p
        self.users = []
        self.socketListener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socketListener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socketListener.bind((self.ip,portp2p))
        self.Log = Log
        self.Chat = Chat
        self.Code = Code
        self.Message = Message
        print('MessageHandler Initialized! Associated port: ' + str(self.portp2p))

    '''
        Handle the connection with a specific user
        when a message is received is passed to the FrontEnd (AMEDEO)
        If the connection is closed the Thread return -1 after sending a signal
        to the front end
    '''
    def receiveMessage(self, conn) :
        msg = conn.recv(self.MSG_LEN)
        msg = msg.decode(self.Code)
        msgs = msg.split('\^')
        user = msgs[0]
        self.users.append(user)
        print('Connection started with ' + user)

        while True:
            try:
                msg = conn.recv(self.MSG_LEN)
                if not msg :
                    raise Exception()
                msg = msg.decode(self.Code)

                dict = json.loads(msg)
                print(msg)
                print(user + ' send : ' + msg)
                if self.Chat is not None:
                    self.Chat.receiveMessage(user, dict['text'], dict['time'])
                #appendToConversation
                self.Message.addMessagetoConversations(user, dict['text'], dict['time'], 1)
            except ArithmeticError:
                print('Connection closed with ' + user)
                return -1
    '''
        In a loop accept new connection with other clients
        and starts a new thread that will handle the single connection
        {this is done in order to distinguish the single connection
         with the specific user}
    '''
    def run(self) :
        while True :
            self.socketListener.listen(50)
            (conn, (ip,port)) = self.socketListener.accept()
            print('Accepted a new connecion')
            t = Thread(target=self.receiveMessage, args=(conn, ))
            t.start()
            print('The client is now connected with : ')
            clientList = ''
            for x in self.users :
                clientList += '- ' + x
            print(clientList)