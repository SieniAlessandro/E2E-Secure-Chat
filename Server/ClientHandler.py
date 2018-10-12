import socket
from threading import Thread
from Log import *
from User import User

class ClientHandler(Thread):
    MSG_LEN = 2048
    #Constructor of the class
    def __init__(self,Conn,ip,port,db,clients,Log):
        Thread.__init__(self)   #Instatation of the thread
        self.HandledUser = User(Conn,ip,0,port,"none")
        self.DB = db
        self.OnlineClients = clients
        self.log = Log
        self.log.log("Client handled has address: "+ self.HandledUser.getIp() +" and port "+str(self.HandledUser.getServerPort()))
    #Method whose listen the message coming from the handled client,showing its content
    def run(self):
        "Function waiting for the message coming from the associate client"
        while True:
            #Receiving the data from the handled client
            try:
                data = self.HandledUser.getSocket().recv(self.MSG_LEN)
            except ConnectionResetError:
                self.log.log("Client had a problem, connection closed")
                return -1
            #Check if the connection is closed analyzing the data (0 means that is close)
            if not data:
                self.log.log("Client disconnected, closing this thread")
                if self.HandledUser in self.OnlineClients.values():
                    del self.OnlineClients[HandledUser.getUserName()]
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
                    self.HandledUser.getSocket().send(("-|1").encode("utf-16"))
                else:
                    self.log.log("Registration failed")
                    #Send to the client that the request has failed
                    self.HandledUser.getSocket().send(("-|0").encode("utf-16"))
            #If the first part is 2, the client want login
            elif msgs[0] == '2':
                self.log.log("A client want to login")
                #Splitting the second part of message in order to obtain all the informations needed to login
                param = msgs[1].split(',')
                response = ""
                params = param[:2]
                #Check if this user is already Logged In
                if self.HandledUser in self.OnlineClients.values():
                    response = "?|"+str(-1)
                #Otherwise control if the parameter sended are correct
                elif self.DB.userIsPresent(*params) == 1:
                    #Inform the client that from now he is logged in
                    response = "?|"+str(1)
                    clientPort = param[-1]
                    UserName = param[0]
                    self.HandledUser.setUserName(UserName)
                    self.HandledUser.setClientPort(clientPort)
                    #print(UserName)
                    #Adding the client to the list of active users
                    self.OnlineClients[UserName] = self.HandledUser
                else:
                    #Inform the client that the login has failed
                    response = "?|"+str(0)
                #Sending the result of the login to the client
                self.HandledUser.getSocket().send(response.encode('utf-16'))
                self.log.log("Active users: "+str(self.OnlineClients))
                msg = self.DB.getMessageByReceiver(self.HandledUser.getUserName())
                if not msg:
                    self.log.log("There are no message for this server")
                    self.HandledUser.getSocket().send("0".encode('utf-16'))
                else:
                    self.log.log("There are several messages to be sended: "+ str(msg))
                    lens = len(msg.split("^/"))
                    self.HandledUser.getSocket().send((str(lens)+"|"+str(msg)).encode('utf-16'))
                self.HandledUser.getSocket().send("0".encode('utf-16'))
            elif msgs[0] == '3':
                self.log.log("A client want to find another user")
                #print("Richiesta di utente online")
                response = ""
                #Check if the clients is logged in
                if self.HandledUser not in self.OnlineClients.values():
                    self.log.log("Cannot found the associate user")
                    response = "!|"+str(-1)
                else:
                    if msgs[1] in self.OnlineClients.keys():
                        #Check if the client asks for its own import ip
                        if self.OnlineClients[msgs[1]] == self.HandledUser:
                            self.log.log("The user want to talk with himself")
                            response = "!|"+str(-2)
                        #Otherwise the server provide the ip of the client and the clientPort
                        else:
                            FoundUser = self.OnlineClients[msgs[1]]
                            response = "!|"+FoundUser.getIp()+":"+str(FoundUser.getClientPort())
                            self.log.log("Ip found:"+response)
                    else:
                        response = "!|"+str(0)
                self.HandledUser.getSocket().send(response.encode('utf-16'))
            elif msgs[0] == '4':
                self.log.log("The user has a massage to be stored on the DB :")
                param = msgs[1].split('/^')
                sender = self.HandledUser.getUserName()
                info = [sender] + param
                if self.DB.insert_message(*info) == 0:
                    self.HandledUser.getSocket().send(".|1".encode('utf-16'))
                else:
                    self.HandledUser.getSocket().send(".|0".encode('utf-16'))
