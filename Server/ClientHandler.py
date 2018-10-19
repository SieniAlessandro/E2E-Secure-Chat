import socket
from threading import Thread
from Log import *
from User import User
import json

JSON = 1
class ClientHandler(Thread):
    """ Used to handle the new user whenever he try to connect to the server.
    This mechanism implies that for each user there is an appropriate thread that handle all the
    requests coming from that clinet
    """
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
        """Waiting for the message coming from the associate client"""
        while self._is_stopped == False:
            #Receiving the data from the handled client
            try:
                data = self.HandledUser.getSocket().recv(self.MSG_LEN)
            except ConnectionResetError:
                self.log.log("Client had a problem, connection closed")
                if self.HandledUser in self.OnlineClients.values():
                    del self.OnlineClients[self.HandledUser.getUserName()]
                return -1
            #Check if the connection is closed analyzing the data (0 means that is close)
            if not data:
                self.log.log("Client disconnected, closing this thread")
                if self.HandledUser in self.OnlineClients.values():
                    del self.OnlineClients[self.HandledUser.getUserName()]
                return -1
            msg = data.decode('utf-16')
            jsonMessage = json.loads(msg)
            #Registration
            if jsonMessage['id'] == "1":
                self.registerUser(jsonMessage)
            #Login
            elif jsonMessage['id'] == "2":
                self.login(jsonMessage)
            #Find the state and the address of another user
            elif jsonMessage['id'] == "3":
                self.findUser(jsonMessage);
            #Store the message waiting for the user
            elif jsonMessage['id'] == "4":
                self.StoreMessage(jsonMessage)

    def login(self,message):
        """Login with inserted credential and search in the Database if the information
        sended are correct, in this case if there are several messagges sended to the user when
        he was offline, the server send them , specifying the sender and also the time (yy-mm-dd hh-mm-ss)"""

        self.log.log("A client want to login")
        response = {}
        #Check if this user is already Logged In
        if self.HandledUser in self.OnlineClients.values():
            response['id'] = "?"
            response['status'] = "-1"
            jsonResponse = json.dumps(response)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
            self.log.log("The request is sended by an user already logged in")
        elif self.DB.userIsPresent(message['username'],message['password']):
            response['id'] = "?"
            response['status'] = "1"
            jsonResponse = json.dumps(response)
            #Informing the user about the success of the login
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
            #Preparing the internal structure used to handle te connection between different clinet
            self.HandledUser.setUserName(message['username'])
            self.HandledUser.setClientPort(message['porta'])
            #Adding the client to the list of active users
            self.OnlineClients[message['username']] = self.HandledUser
            self.log.log("Active users: "+str(self.OnlineClients))
            #Obtaining all the messages waiting for that user
            msg = self.DB.getMessageByReceiver(self.HandledUser.getUserName())
            if len(msg.keys()) == 0:
                self.log.log("There are no message for this client")
                response['id'] = "0"
                jsonResponse = json.dumps(response)
                #Informing the user that there are no message for him
                self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
            else:
                self.log.log("There are several messages to be sended: "+ str(msg))
                lens = len(msg)
                response = {}
                response['id'] = str(lens)
                response['messages'] = {}
                response['messages'] = msg
                jsonResponse = json.dumps(response)
                #Removing the messagess previously obtained
                self.remove_waiting_messages_by_receiver(self.HandledUser.getUserName())
                self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
        else:
            response = {}
            response['id'] = "?"
            response['status'] = "0"
            jsonResponse = json.dumps(response)
            self.log.log("Login Failed")
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))

    def registerUser(self,message):
        """ Insert the information of the user in the database, checking if there is another user with the same Username
        and sending back the result"""
        self.log.log("A client want to register")
        response = {}
        if (self.DB.insert_user(message['user'],message['password'],message['name'],message['surname'],message['email'],message['key']) == 0):
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

    def StoreMessage(self,message):
        """Store the message in the database waiting that the client come back online"""
        self.log.log("The user has a massage to be stored on the DB :")
        sender = self.HandledUser.getUserName()
        response = {}
        if self.DB.insert_message(sender,message['Receiver'],message['Text'],message['Time']) == 0:
            response['id'] = "."
            response['status'] = "1"
            jsonResponse = json.dumps(response)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))
        else:
            response['id'] = "."
            reponse['status'] = "0"
            jsonResponse = json.dumps(response)
            self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))

    def findUser(self,message):
        """ Find the information about the user (IPaddress:clientPort) related to the username passed as parameter"""
        self.log.log("A client want to find another user")
        response = {}
        if self.HandledUser not in self.OnlineClients.values():
            self.log.log("Cannot found the associate user")
            response['id'] = "!"
            response['status'] = "-1"
        else:
            if message['username'] in self.OnlineClients.keys():
                #Check if the client asks for its own import ip
                if self.OnlineClients[message['username']] == self.HandledUser:
                    self.log.log("The user want to talk with himself")
                    response['id'] = "!"
                    response['status'] = "-2"
                 #Otherwise the server provide the ip of the client and the clientPort
                else:
                    FoundUser = self.OnlineClients[message['username']]
                    response['id'] = "!"
                    response['status'] = FoundUser.getIp()+":"+str(FoundUser.getClientPort())
                    self.log.log("Ip found:"+response['status'])
            else:
                #Check if the receiver is not registered
                if self.DB.userIsRegistered(message['username']) == 0:
                    response['id'] = "!"
                    response['status'] = "-3"
                    self.log.log("User requested not found")
                else:
                    self.log.log("Store the message to "+message['username'])
                    response['id'] = "!"
                    response['status'] = "0"
        jsonResponse = json.dumps(response)
        self.HandledUser.getSocket().send(jsonResponse.encode('utf-16'))

    def getHandledUser(self):
        """This function gets back the username associate to the handled client"""
        return self.HandledUser.getUserName()
