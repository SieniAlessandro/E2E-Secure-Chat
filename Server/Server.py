import socket
from Database.Database import Database
from threading import Thread
from ClientHandler import *
from Log import *
import signal, os
from os import system, name
import sys
from User import User
from XMLHandler import XMLHandler
from Security.Security import Security

class Server:
    """
        Handle the global information, and the connection with the database
    """
    def __init__(self):
        self.XML = XMLHandler()
        self.Users = {}
        self.ActiveThreads = []
        self.ip = "0.0.0.0"
        self.port = self.XML.getServerPort()
        self.sec = Security(self.XML.getPemPath(),self.XML.getBackupPemPath())
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
        self.server.bind((self.ip,self.port))
        self.DB = Database(_host = self.XML.getDatabaseAddress(),\
                           _port = self.XML.getDatabasePort(),\
                           _user = self.XML.getDatabaseUser(),\
                           _password = self.XML.getDatabasePwd(),\
                           _db = self.XML.getDatabaseName());
        self.Log = Log(self.XML.getEnableLog(),self.XML.GetLogPath())
        self.Log.log("Server Initialized")
    def start(self):
        """
            Create a new thread able to handle the administrator request (like see the number of active thread or online users)
        """
        #Starting the thread able to handle the administrator request
        t2 = threading.Thread(target=self.handleServer)
        t2.start()
        self.ActiveThreads.append(t2)
        #Listen continously
        while True:
            self.server.listen(50)
            self.Log.log("Waiting for connections...")
            #Obtaining the parameters like the socket and the address/port of the incoming connection
            (conn, (ip,port)) = self.server.accept()
            #Creating a new thread able to handle the new connection with the client
            newClient = ClientHandler(conn,ip,port,self.DB,self.Users,self.Log,self.XML);
            #Starting the new thread
            newClient.start()
            self.ActiveThreads.append(newClient)
    def handleServer(self):
        """
            Handle the administrator request
        """
        choice = 1
        while choice != 0:
            try:
                choice = int(input("What you want to do?\n1)Count online user \n2)Count Active Thread\n3)Print Public Key\n)Other key to close the server:\n"))
            except ValueError:
                self.close()
            if choice == 1:
                if len(self.Users.values()) == 0:
                    print ("There are no online users")
                else:
                    for User in self.Users.values():
                        print("UserName: "+User.getUserName()+" has address: "+User.getIp()+" and a Client port: "+str(User.getClientPort()))
            elif choice == 2:
                print("Actually there are %d active thread" % (len(threading.enumerate())))
            elif choice == 3:
                print(self.sec.getSerializedPublicKey().decode('utf-8'))
            else:
                print("Ok i'll close the server")
                self.close()

    def close(self):
        """
            Close all the socket and close the connection with the database
        """
        self.Log.log("Server Closed")
        for User in self.Users.values():
            User.getSocket.shutdown(socket.SHUT_RDWR)
            User.getSocket.close()
        self.DB.close_connection()
        self.Log.closeFile()
        os._exit(0)
