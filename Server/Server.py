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
<<<<<<< HEAD
        print ("Server iniziallizato")
=======
        print("Server iniziallizato")
>>>>>>> 4899d035486905a5d5e9509df4d4db1711d3f94e

    def listen(self):
        while True:
            self.server.listen(50)
<<<<<<< HEAD
            print ("In attesa di richieste...")
            (conn, (ip,port)) = self.server.accept()
            print ("Nuova richiesta arrivata..")
=======
            print("In attesa di richieste...")
            (conn, (ip,port)) = self.server.accept()
            print("Nuova richiesta arrivata...")
>>>>>>> 4899d035486905a5d5e9509df4d4db1711d3f94e
            newClient = ClientHandler(conn,ip,port);
            newClient.start();
            self.clients.append(newClient);
