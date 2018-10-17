import socket
from threading import Thread
from Log import *
from User import User
import json

JSON = 1
class ClientHandler(Thread):
    MSG_LEN = 2048
    #Constructor of the class
    def __init__(self,Conn,ip,port,db,clients,Log,ActiveThreads):
        Thread.__init__(self)   #Instatation of the thread
        self.HandledUser = User(Conn,ip,0,port,"none")
        self.DB = db
        self.OnlineClients = clients
        self.log = Log
        self.ActiveThreads = ActiveThreads
        self.log.log("Client handled has address: "+ self.HandledUser.getIp() +" and port "+str(self.HandledUser.getServerPort()))
    #Method whose listen the message coming from the handled client,showing its content
    def run(self):
        "Function waiting for the message coming from the associate client"
        while self._is_stopped == False:
            #Receiving the data from the handled client
            try:
                data = self.HandledUser.getSocket().recv(self.MSG_LEN)
            except ConnectionResetError:
                self.log.log("Client had a problem, connection closed")
                if self.HandledUser in self.OnlineClients.values():
                    del self.OnlineClients[self.HandledUser.getUserName()]
                #ActiveThreads = ActiveThreads - 1
                return -1
            #Check if the connection is closed analyzing the data (0 means that is close)
            if not data:
                self.log.log("Client disconnected, closing this thread")
                if self.HandledUser in self.OnlineClients.values():
                    del self.OnlineClients[self.HandledUser.getUserName()]
                    #ActiveThreads = ActiveThreads - 1
                return -1
            msg = data.decode('utf-16')

            jsonMessage = json.loads(msg)
            print(msg)

            #Registration
            if jsonMessage['id'] == "1":
                self.registerUser(jsonMessage)
            #Login
            elif jsonMessage['id'] == "2":
                self.login(jsonMessage)
            elif jsonMessage['id'] == "3":
                self.findUser(jsonMessage);
            elif jsonMessage['id'] == "4":
                self.StoreMessage(jsonMessage)
    def login(self,msgs):
        self.log.log("A client want to login")
        response = {}
        #Check if this user is already Logged In
        if self.HandledUser in self.OnlineClients.values():
            response['id'] = "?"
            response['status'] = "-1"
            jsonResponse = json.dumps(response)
            print(jsonResponse)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
        elif self.DB.userIsPresent(msgs['username'],msgs['password']):
            response['id'] = "?"
            response['status'] = "1"
            jsonResponse = json.dumps(response)
            print(jsonResponse)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
            self.HandledUser.setUserName(msgs['username'])
            self.HandledUser.setClientPort(msgs['porta'])
            #Adding the client to the list of active users
            self.OnlineClients[msgs['username']] = self.HandledUser
            self.log.log("Active users: "+str(self.OnlineClients))
            msg = self.DB.getMessageByReceiver(self.HandledUser.getUserName())
            if len(msg.keys()) == 0:
                self.log.log("There are no message for this client")
                response['id'] = "0"
                jsonResponse = json.dumps(response)
                jsonResponse = json.dumps(response)
                self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
                print(jsonResponse)
                #self.HandledUser.getSocket().send("0".encode('utf-16'))
            else:
                self.log.log("There are several messages to be sended: "+ str(msg))
                lens = len(msg)
                response = {}
                response['id'] = str(lens)
                response['messages'] = {}
                response['messages'] = msg
                jsonResponse = json.dumps(response)
                print(jsonResponse)
                self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))

    def registerUser(self,msgs):
        self.log.log("A client want to register")
        response = {}
        if (self.DB.insert_user(msgs['user'],msgs['password'],msgs['name'],msgs['surname'],msgs['email'],msgs['key']) == 0):
            self.log.log("Registration succeded")
            #Send to the client that the request has succeded
            response['id'] = "-"
            response['status'] = "1"
            jsonMessage = json.dumps(response)
            self.HandledUser.getSocket().send(jsonMessage.encode('utf-16'))
        else:
            self.log.log("Registration failed")
            #Send to the client that the request has failed
            response['id'] = "-"
            response['status'] = "0"
            jsonMessage = json.dumps(response)
            self.HandledUser.getSocket().send(jsonMessage.encode('utf-16'))

    def StoreMessage(self,msgs):
        self.log.log("The user has a massage to be stored on the DB :")
        sender = self.HandledUser.getUserName()
        response = {}
        if self.DB.insert_message(sender,msgs['Receiver'],msgs['Text'],msgs['Time']) == 0:
            response['id'] = "."
            response['status'] = "1"
            jsonResponse = json.dumps(response)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
        else:
            response['id'] = "."
            reponse['status'] = "0"
            jsonResponse = json.dumps(response)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))


    def findUser(self,msgs):
        self.log.log("A client want to find another user")
        response = {}
        if self.HandledUser not in self.OnlineClients.values():
            self.log.log("Cannot found the associate user")
            response['id'] = "!"
            response['status'] = "-1"
        else:
            if msgs['username'] in self.OnlineClients.keys():
                #Check if the client asks for its own import ip
                if self.OnlineClients[msgs['username']] == self.HandledUser:
                    self.log.log("The user want to talk with himself")
                    response['id'] = "!"
                    response['status'] = "-2"
                 #Otherwise the server provide the ip of the client and the clientPort
                else:
                    FoundUser = self.OnlineClients[msgs['username']]
                    #response = "!|"+FoundUser.getIp()+":"+str(FoundUser.getClientPort())
                    response['id'] = "!"
                    response['status'] = FoundUser.getIp()+":"+str(FoundUser.getClientPort())
                    #response = "!|127.0.0.1"+":"+str(FoundUser.getClientPort())
                    self.log.log("Ip found:"+response['status'])
            else:
                #Check if the receiver is not registered
                if self.DB.userIsRegistered(msgs['username']) == 0:
                    #response ="!|"+str(-3)
                    response['id'] = "!"
                    response['status'] = "-3"
                    self.log.log("User requested not found")
                else:
                    self.log.log("Store the message to "+msgs['username'])
                    response['id'] = "!"
                    response['status'] = "0"
        jsonResponse = json.dumps(response)
        self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))

    def getHandledUser(self):
        return self.HandledUser.getUserName()
