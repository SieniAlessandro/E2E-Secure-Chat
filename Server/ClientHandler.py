import socket
from threading import Thread


class ClientHandler(Thread):
    MSG_LEN = 2048
    #Constructor of the class
    #Parameters:
    def __init__(self,conn,ip,port):
        Thread.__init__(self)   #Instatation of the thread
        self.ip = ip
        self.port = port
        self.conn = conn
        print ("Client gestito all'indirizzo "+ self.ip +" porta "+str(self.port))

    #Method whose listen the message coming from the handled client,showing its content
    def run(self):
        while True:
            data = self.conn.recv(self.MSG_LEN)
            print ("Message receveid: "+data)
