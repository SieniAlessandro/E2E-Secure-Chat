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
    def start(self):
        #Listen continously 
        while True:
            self.server.listen(50)
            self.Log.log("Waiting for connections...")
            print ("In attesa di richieste...")
            #Obtaining the parameters like the socket and the address/port of the incoming connection
            (conn, (ip,port)) = self.server.accept()
            #Creating a new thread able to handle the new connection with the client
            newClient = ClientHandler(conn,ip,port,self.DB,self.Users,self.Log);
            #Starting the new thread
            newClient.start();
            #Appending the new thread to the list of active thread in order to manage them if it is necessary
            self.Threads.append(newClient);
