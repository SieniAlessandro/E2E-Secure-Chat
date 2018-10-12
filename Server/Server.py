import socket
from Database.Database import Database
from threading import Thread
from ClientHandler import *
from Log import *
import signal, os
from os import system, name
import sys
from User import User

class Server:
    def __init__(self,port):
        self.Users = {}
        self.ActiveThreads = 0
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
        t2.start()
        self.ActiveThreads = self.ActiveThreads + 1
        #Listen continously
        while True:
            self.server.listen(50)
            self.Log.log("Waiting for connections...")
            #Obtaining the parameters like the socket and the address/port of the incoming connection
            (conn, (ip,port)) = self.server.accept()
            #Creating a new thread able to handle the new connection with the client
            newClient = ClientHandler(conn,ip,port,self.DB,self.Users,self.Log,self.ActiveThreads);
            #Starting the new thread
            newClient.start()
            #Appending the new thread to the list of active thread in order to manage them if it is necessary
            self.ActiveThreads = self.ActiveThreads + 1

    def handleServer(self):
        choice = 1
        while choice != 0:
            try:
                choice = int(input("What you want to do?\n1) Count online user \n2)Ban an user \n3)Count Active Thread\n4)Close Server\n:"))
            except ValueError:
                print("Ok i'll close the server")
                os._exit(0)
            if choice == 1:
                if len(self.Users.values()) == 0:
                    print ("There are no online users")
                else:
                    for User in self.Users.values():
                        print("UserName: "+User.getUserName()+" has address: "+User.getIp()+" and a Client port: "+str(User.getClientPort()))
            elif choice == 2:
                print("Actually i can't ban any user")
            elif choice == 3:
                print("Actually there are "+str(self.ActiveThreads)+" active threads")
            else:
                print("Ok i'll close the server")
                os._exit(0)
    def close(self):
        self.Log.log("Server Closed")
        for User in self.Users.values():
            User.getSocket.close()
        self.DB.close_connection()
