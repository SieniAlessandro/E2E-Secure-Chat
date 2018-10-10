import socket
from Database.Database import Database
from threading import Thread
from ClientHandler import *
from Log import *
import signal, os
from os import system, name
import sys

class Server:
    def __init__(self,port):
        self.Users = {}
        self.Threads = []
        self.sockets =[]
        self.ip = "0.0.0.0"
        self.port = port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
        self.server.bind((self.ip,self.port))
        self.DB = Database('localhost',3306,'root','rootroot','messaggistica_mps');
        self.Log = Log()
        self.state = 1
        print ("Server iniziallizato")
        self.Log.log("Server Initialized")
    def start(self):
        t2 = threading.Thread(target=self.handleServer)
        self.Threads.append(t2)
        t2.start()
        #Listen continously
        while True:
            self.server.listen(50)
            self.Log.log("Waiting for connections...")
            #print ("In attesa di richieste...")
            #Obtaining the parameters like the socket and the address/port of the incoming connection
            (conn, (ip,port)) = self.server.accept()
            #Creating a new thread able to handle the new connection with the client
            newClient = ClientHandler(conn,ip,port,self.DB,self.Users,self.Log);
            #Starting the new thread
            newClient.start();
            #Appending the new thread to the list of active thread in order to manage them if it is necessary
            self.Threads.append(newClient);
            self.sockets.append(conn)

    def handleServer(self):
        choice = 1
        while choice != 0:
            try:
                choice = int(input("What you want to do?\n1) Count online user \n2)Count thread active \n3)Ban an user \n4)Close Server\n:"))
            except ValueError:
                print("Ok i'll close the server")
                os._exit(0)
            if choice == 1:
                if len(self.Users.values()):
                    print ("There are no online users")
                else:
                    for user,addr in zip(self.Users.values(),self.Users.keys()):
                        print("User: "+str(user)+" has address: "+str(addr))
            elif choice == 2:
                print ("Actually there are "+str(len(self.Threads)) +" working threads")
            elif choice == 3:
                print("Actually i can't ban any user")
            else:
                print("Ok i'll close the server")
                os._exit(0)
    def close(self):
        self.Log.log("Server Closed")
        for conn in self.sockets:
            conn.close()
        self.DB.close_connection()
