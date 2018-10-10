import socket
from threading import Thread

class MessageHandler(Thread) :
    MSG_LEN = 2048
    PORT_P2P = 7000
    #Constructor
    def __init__(self):
        Thread.__init__(self)   #Instatation of the thread
        self.ip = "0.0.0.0"
        self.port = self.PORT_P2P
        self.socketListener = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        self.socketListener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
        self.socketListener.bind((self.ip,self.port))

    def receiveMessage(self, conn):
        user = conn.recv(self.MSG_LEN)
        while True:
            msg = conn.recv(self.MSG_LEN)
            msg = msg.decode('utf-16')
            print(msg)
            #send to Amedeo

    def run(self) :
        print('MessageHandler is Started!')
        while True :
            self.socketListener.listen(50)
            (conn, (ip,port)) = self.server.accept()
            threading.Thread(target=self.receiveMessage, args={conn})
            #Starting the new thread
            newClient.start();
            #Appending the new thread to the list of active thread in order to manage them if it is necessary
