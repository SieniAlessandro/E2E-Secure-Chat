import socket
from threading import Thread
from ClientHandler import *


class Server:
    def __init__(self,port):
        self.ip = "0.0.0.0"
        self.port = port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
        self.server.bind((self.ip,self.port))
        self.clients = []
        print ("Server iniziallizato")

    def listen(self):
        while True:
            self.server.listen(50)
            print ("In attesa di richieste...")
            (conn, (ip,port)) = self.server.accept()
            print ("Nuova richiesta arrivata..")
            newClient = ClientHandler(conn,ip,port);
            newClient.start();
            self.clients.append(newClient);
