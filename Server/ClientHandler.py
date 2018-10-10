import socket
from threading import Thread
from Log import *

class ClientHandler(Thread):
    MSG_LEN = 2048
    #Constructor of the class
    def __init__(self,Conn,ip,port,db,clients,Log):
        Thread.__init__(self)   #Instatation of the thread
        self.ip = ip
        self.port = port
        self.conn = Conn
        self.DB = db
        self.OnlineClients = clients
        self.log = Log
        print ("Client gestito all'indirizzo "+ self.ip +" porta "+str(self.port))
        self.log.log("Client handled has address: "+ self.ip +" and port "+str(self.port))
    #Method whose listen the message coming from the handled client,showing its content
    def run(self):
        while True:
            #Receiving the data from the handled client
            data = self.conn.recv(self.MSG_LEN)
            #Check if the connection is closed analyzing the data (0 means that is close)
            if not data:
                self.log.log("Client disconnected, closing this thread")
                #print("Client disconnesso")
                if self.ip in self.OnlineClients.values():
                    self.OnlineClients.remove(self.ip)
                return -1
            #Decoding the received data to obtain a string
            msg = data.decode('utf-16')

            #print ("Message received: "+msg)

            #Spliting the whole message to retrieve the type of request and the content of that request
            msgs = msg.split('|')
            #If the first part is 1, the client want to register as new user
            if msgs[0] == "1":
                self.log.log("A client want to register")
                print ("Registrazione")
                #Splitting the second part of message in order to obtain all the informations needed to register a new user
                param = msgs[1].split(',')
                #Use of the class Database with the appropriate method to insert the new user, checking if the insertion
                #has completed correctly
                if (self.DB.insert_user(*param) == 0):
                    self.log.log("Registration succeded")
                    #Send to the client that the request has succeded
                    self.conn.send(("Ti ho registrato "+param[0]).encode('utf-16'))
                else:
                    self.log.log("Registration failed")
                    #Send to the client that the request has failed
                    self.conn.send("Errore nella registrazione".encode('utf-16'))
            #If the first part is 2, the client want login
            elif msgs[0] == '2':
                self.log.log("A client want to login")
                print("Login")
                #Splitting the second part of message in order to obtain all the informations needed to login
                param = msgs[1].split(',')
                response = ""
                #Check if this user is already Logged In
                if self.ip in self.OnlineClients.values:
                    response = "?|"+str(-1)
                #Otherwise control if the parameter sended are correct
                elif self.DB.userIsPresent(*param) == 1:
                    #Inform the client that from now he is logged in
                    response = "?|"+str(1)
                    #Adding the client to the list of active users
                    self.OnlineClients[param[0]] = self.ip
                else:
                    #Inform the client that the login has failed
                    response = "?|"+str(0)
                #Sending the result of the login to the client
                self.conn.send(response.encode('utf-16'))
                self.log.log("Active users: "+str(self.OnlineClients))
            elif msgs[0] == '3':
                self.log.log("A client want to find another user")
                #print("Richiesta di utente online")
                response = ""
                #Check if the clients is logged in
                if self.ip not in self.OnlineClients.values():
                    response = "!|"+str(-1)
                else:
                    if msgs[1] in self.OnlineClients.keys():
                        #Check if the client asks for its own import ip
                        if self.OnlineClients[msgs[1]] == self.ip:
                            response = "!|"+str(-2)
                        #Otherwise the server provide the ip of the client
                        else:
                            response = "!|"+self.OnlineClients[msgs[1]]
                    else:
                        response = "!|"+str(0)
                self.conn.send(response.encode('utf-16'))
            elif msgs[0] == '4':
                self.log.log(str(threading.get_ident())+"The user has a massage to be stored on the DB")
                param = msgs[1].split(',')
                sender = list(self.OnlineClients)[list(self.OnlineClients.values()).index(self.ip)]
                print(sender)
