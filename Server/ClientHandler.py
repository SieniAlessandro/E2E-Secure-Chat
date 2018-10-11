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
        self.ClientPort = 0
        self.DB = db
        self.OnlineClients = clients
        self.log = Log
        self.log.log("Client handled has address: "+ self.ip +" and port "+str(self.port))
    #Method whose listen the message coming from the handled client,showing its content
    def run(self):
        "Function waiting for the message coming from the associate client"
        while True:
            #Receiving the data from the handled client
            try:
                data = self.conn.recv(self.MSG_LEN)
            except ConnectionResetError:
                self.log.log("Client had a problem, connection closed")
                return -1
            #Check if the connection is closed analyzing the data (0 means that is close)
            if not data:
                self.log.log("Client disconnected, closing this thread")
                if self.ip+":"+str(self.ClientPort)+"|"+str(self.port) in self.OnlineClients.values():
                    sender = list(self.OnlineClients)[list(self.OnlineClients.values()).index(self.ip+":"+str(self.ClientPort)+"|"+str(self.port))]
                    del self.OnlineClients[sender]
                return -1
            #Decoding the received data to obtain a string
            msg = data.decode('utf-16')

            #Spliting the whole message to retrieve the type of request and the content of that request
            msgs = msg.split('|')
            #If the first part is 1, the client want to register as new user
            if msgs[0] == "1":
                self.log.log("A client want to register")
                #Splitting the second part of message in order to obtain all the informations needed to register a new user
                param = msgs[1].split(',')
                #Use of the class Database with the appropriate method to insert the new user, checking if the insertion
                #has completed correctly
                if (self.DB.insert_user(*param) == 0):
                    self.log.log("Registration succeded")
                    #Send to the client that the request has succeded
                    self.conn.send(("-|1").encode("utf-16"))
                else:
                    self.log.log("Registration failed")
                    #Send to the client that the request has failed
                    self.conn.send(("-|0").encode("utf-16"))
            #If the first part is 2, the client want login
            elif msgs[0] == '2':
                self.log.log("A client want to login")
                #Splitting the second part of message in order to obtain all the informations needed to login
                param = msgs[1].split(',')
                response = ""
                params = param[:2]
                self.ClientPort = param[2]
                print(params)
                print(self.ClientPort)
                #Check if this user is already Logged In
                if self.ip+":"+str(self.ClientPort)+"|"+str(self.port) in self.OnlineClients.values():
                    response = "?|"+str(-1)
                #Otherwise control if the parameter sended are correct

                elif self.DB.userIsPresent(*params) == 1:
                    #Inform the client that from now he is logged in
                    response = "?|"+str(1)
                    self.ClientPort = param[-1]
                    #Adding the client to the list of active users
                    self.OnlineClients[param[0]] = self.ip+":"+str(self.ClientPort)+"|"+str(self.port)
                else:
                    #Inform the client that the login has failed
                    response = "?|"+str(0)
                #Sending the result of the login to the client
                self.conn.send(response.encode('utf-16'))
                self.log.log("Active users: "+str(self.OnlineClients))
                user = list(self.OnlineClients)[list(self.OnlineClients.values()).index(self.ip+":"+str(self.ClientPort)+"|"+str(self.port))]
                msg = self.DB.getMessageByReceiver(user)
                if not msg:
                    self.log.log("There are no message for this server")
                    self.conn.send("0".encode('utf-16'))
                else:
                    self.log.log("There are several messages to be sended: "+ str(msg))
                    lens = len(msg.split("^/"))
                    self.conn.send((str(lens)+"|"+str(msg)).encode('utf-16'))

                self.conn.send("0".encode('utf-16'))
            elif msgs[0] == '3':
                self.log.log("A client want to find another user")
                #print("Richiesta di utente online")
                response = ""
                #Check if the clients is logged in
                if self.ip+"|"+str(self.port) not in self.OnlineClients.values():
                    self.log.log("Cannot found the associate user")
                    response = "!|"+str(-1)
                else:
                    if msgs[1] in self.OnlineClients.keys():
                        #Check if the client asks for its own import ip
                        if self.OnlineClients[msgs[1]] == (self.ip+"|"+str(self.port)):
                            self.log.log("The user want to talk with himself")
                            response = "!|"+str(-2)
                        #Otherwise the server provide the ip of the client
                        else:

                            response = "!|"+self.OnlineClients[msgs[1]].split("|")[0]
                            self.log.log("Ip found:"+response)
                    else:
                        response = "!|"+str(0)
                self.conn.send(response.encode('utf-16'))
            elif msgs[0] == '4':
                self.log.log("The user has a massage to be stored on the DB :")
                param = msgs[1].split('/^')
                sender = list(self.OnlineClients)[list(self.OnlineClients.values()).index(self.ip+"|"+str(self.port))]
                info = [sender] + param
                if self.DB.insert_message(*info) == 0:
                    self.conn.send(".|1".encode('utf-16'))
                else:
                    self.conn.send(".|0".encode('utf-16'))
