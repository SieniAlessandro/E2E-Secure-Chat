import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *


class ConnectionHandler(Thread) :
    MSG_LEN = 4096
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
        self.Log.log('MessageHandler Initialized! Associated port: ' + str(self.portp2p))

    '''
        Handle the connection with a specific user
        when a message is received is passed to the FrontEnd (AMEDEO)
        If the connection is closed the Thread return -1 after sending a signal
        to the front end
    '''
    def receiveMessage(self, conn) :
        #self.Log.log('Connection started with ' + str(user))
        while True:
            try:
                #length = conn.recv(self.MSG_LEN)
                msg = conn.recv(self.MSG_LEN)
                #if not msg :
                #    raise Exception()

                msg = msg.decode(self.Code)

                #print('Message received: ' + msg + ' length : ' + length)
                dict = json.loads(msg)

                self.Log.log(dict['sender'] + ' send : ' + msg)
                if self.Chat is not None:
                    self.Chat.receiveMessage(dict['sender'], dict['text'], dict['time'])
                #appendToConversation
                self.Message.addMessagetoConversations(dict['sender'], dict['text'], dict['time'], 1)
            except Exception as e:
                #print(e)
                self.Log.log('Connection closed')
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
            self.Log.log('Accepted a new connecion')
            t = Thread(target=self.receiveMessage, args=(conn, ))
            t.start()
