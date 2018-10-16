import socket
from threading import Thread
from Log import *
from User import User
import json

JSON = 1
class ClientHandler(Thread):
    MSG_LEN = 2048
    #Constructor of the class
    def __init__(self,Conn,ip,port,db,clients,Log,ActiveThreads,Json):
        Thread.__init__(self)   #Instatation of the thread
        self.HandledUser = User(Conn,ip,0,port,"none")
        self.json = Json
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
            if self.json:
                jsonMessage = json.loads(msg)
                #Registration
                if jsonMessage['id'] == "1":
                    self.registerUser(jsonMessage)
                #Login
                elif jsonMessage['id'] == "2":
                    self.login(jsonMessage)
            else:
                #Decoding the received data to obtain a string

                #Spliting the whole message to retrieve the type of request and the content of that request
                msgs = msg.split('|')
                #If the first part is 1, the client want to register as new user

                if msgs[0] == "1":
                    self.registerUser(msgs)
                #If the first part is 2, the client want login
                elif msgs[0] == '2':
                    self.login(msgs)
                #If the first part is 3, the client want to know if the user is online
                elif msgs[0] == '3':
                    self.findUser(msgs)
                #If the first part is 4, the client want to store the message waiting for the back online of the receiver
                elif msgs[0] == '4':
                    self.StoreMessage(msgs)

    def login(self,msgs):
        self.log.log("A client want to login")
        if self.json:
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
                print(jsonResponse)
                self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
                self.HandledUser.setUserName(UserName)
                self.HandledUser.setClientPort(clientPort)
                #Adding the client to the list of active users
                self.OnlineClients[UserName] = self.HandledUser
                self.log.log("Active users: "+str(self.OnlineClients))
                msg = self.DB.getMessageByReceiver(self.HandledUser.getUserName())
                if len(msg) == 0:
                    self.log.log("There are no message for this client")
                    self.HandledUser.getSocket().send("0".encode('utf-16'))
                else:
                    self.log.log("There are several messages to be sended: "+ str(msg))
                    lens = len(msg)
                    response = {}
                    response['number'] = str(lens)
                    response['messages'] = {}
                    response['messages'] = msg
                    jsonResponse = json.dumps(response)
                    print(jsonResponse)
                    self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
        else:
            #Splitting the second part of message in order to obtain all the informations needed to login
            param = msgs[1].split(',')
            response = ""
            params = param[:2]
            #Check if this user is already Logged In
            if self.HandledUser in self.OnlineClients.values():
                response = "?|"+str(-1)
                self.HandledUser.getSocket().send(response.encode('utf-16'))
            #Otherwise control if the parameter sended are correct
            elif self.DB.userIsPresent(*params) == 1:
                #Inform the client that from now he is logged in
                response = "?|"+str(1)
                self.HandledUser.getSocket().send(response.encode('utf-16'))
                clientPort = param[-1]
                UserName = param[0]
                self.HandledUser.setUserName(UserName)
                self.HandledUser.setClientPort(clientPort)
                #Adding the client to the list of active users
                self.OnlineClients[UserName] = self.HandledUser
                self.log.log("Active users: "+str(self.OnlineClients))
                msg = self.DB.getMessageByReceiver(self.HandledUser.getUserName())
                if not msg:
                    self.log.log("There are no message for this client")
                    self.HandledUser.getSocket().send("0".encode('utf-16'))
                else:
                    self.log.log("There are several messages to be sended: "+ str(msg))
                    lens = len(msg.split("^/"))
                    self.HandledUser.getSocket().send((str(lens)+"|"+str(msg)).encode('utf-16'))
            else:
                #Inform the client that the login has failed
                response = "?|"+str(0)
                self.HandledUser.getSocket().send(response.encode('utf-16'))
                #Sending the result of the login to the client

    def registerUser(self,msgs):
        self.log.log("A client want to register")
        if self.json:
            respone = {}
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
        else:
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

    def StoreMessage(self,msgs):
        self.log.log("The user has a massage to be stored on the DB :")
        param = msgs[1].split('/^')
        sender = self.HandledUser.getUserName()
        info = [sender] + param
        if self.DB.insert_message(*info) == 0:
            self.HandledUser.getSocket().send(".|1".encode('utf-16'))
        else:
            self.HandledUser.getSocket().send(".|0".encode('utf-16'))

    def findUser(self,msgs):
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
                    #response = "!|127.0.0.1"+":"+str(FoundUser.getClientPort())
                    self.log.log("Ip found:"+response)
            else:
                #Check if the receiver is not registered
                if self.DB.userIsRegistered(msgs[1]) == 0:
                    response ="!|"+str(-3)
                    self.log.log("User requested not found:"+response)
                else:
                    self.log.log("Store the message to "+msgs[1])
                    response = "!|"+str(0)
        self.HandledUser.getSocket().send(response.encode('utf-16'))

    def getHandledUser(self):
        return self.HandledUser.getUserName()
