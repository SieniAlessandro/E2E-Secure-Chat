import socket
import random
import threading
from client import *
from threading import Thread


class MessageHandler(Thread) :
    MSG_LEN = 2048
    #Constructor
    def __init__(self, portp2p) :
        Thread.__init__(self)
        self.ip = "0.0.0.0"

        self.socketListener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socketListener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socketListener.bind((self.ip,portp2p))


    def receiveMessage(self, conn) :
        print('Started the receivingMessage Thread!!!\n')
        #try :
        user = conn.recv(self.MSG_LEN)
        user = user.decode('utf-16')
        print('Connection started with ' + user)
        #except :
        #    print('An exception is occurred')
        while True:
            msg = conn.recv(self.MSG_LEN)
            msg = msg.decode('utf-16')
            print(user + ' send : ' + msg)
            #send to Amedeo

    def run(self) :
        print('MessageHandler is Started!')
        while True :
            self.socketListener.listen(50)
            (conn, (ip,port)) = self.socketListener.accept()
            print('Accepted a new connecion')
            t = Thread(target=self.receiveMessage, args=(conn, ))
            t.start()
