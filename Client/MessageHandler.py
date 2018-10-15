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
        self.users = []
        self.socketListener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socketListener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socketListener.bind((self.ip,portp2p))


    def receiveMessage(self, conn) :
        print('Started the receiving Message Thread!!!\n')
        #try :
        msg = conn.recv(self.MSG_LEN)
        msg = msg.decode('utf-16')
        msgs = msg.split('\^')
        user = msgs[0]
        self.users.append(user)
        print('Connection started with ' + user)
        if len(msgs) > 1:
            print(user + ' send : ' + msgs[1])
        #except :
        #    print('An exception is occurred')
        while True:
            try:
                msg = conn.recv(self.MSG_LEN)
                if not msg
                    raise Exception()
                msg = msg.decode('utf-16')
                print(user + ' send : ' + msg)
            #send to Amedeo
            except:
                print('The user has disconnected')
                return

    def run(self) :
        print('MessageHandler is Started!')
        while True :
            self.socketListener.listen(50)
            print('Waiting for connection')
            (conn, (ip,port)) = self.socketListener.accept()
            print('Accepted a new connecion')
            t = Thread(target=self.receiveMessage, args=(conn, ))
            t.start()
            print('The client is connected with : ')
            for x in self.users :
                print('\t- ' + x)
