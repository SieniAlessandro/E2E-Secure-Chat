import socket
from Database.Database import Database
from threading import Thread
from ClientHandler import *
from Log import *

class Server:
    def __init__(self,port):
        self.ip = "0.0.0.0"
        self.port = port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
        self.server.bind((self.ip,self.port))
        self.Users = {}
        self.Threads = []
        self.DB = Database('localhost',3306,'root','rootroot','messaggistica_mps');
        self.Log = Log()
        print ("Server iniziallizato")
        self.Log.log("Server Initialized")
    def listen(self):
        while True:
            self.server.listen(50)
            self.Log.log("Waiting for connections...")
            print ("In attesa di richieste...")
            (conn, (ip,port)) = self.server.accept()
            newClient = ClientHandler(conn,ip,port,self.DB,self.Users,self.Log);
            newClient.start();
            self.Threads.append(newClient);
