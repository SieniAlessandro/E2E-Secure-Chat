#from socket import AF_INET, socket, SOCK_STREAM
import socket
import json
import datetime
from threading import Thread
from Message import *
from ConnectionHandler import *
from Log import *
from XMLClientHandler import *
from Security.SecurityClient import *
import os
import binascii
import zlib

class Client:
    """
    Back end of the client
    """
    BUFFER_SIZE = 2048*1024
    CODE_TYPE = 'utf-8'
    socketClient = {}

    def __init__(self, chat = None):
        """
            The BackEnd of the client, initialize the structures used for the connection with
            the server, for the Security, for handling json messages, to pass the data to the frontEnd

            :type chat: ChatList or None, it is None only if the GUI is not used
            :param chat: used to insert the messages in the front end of the client
        """
        self.XML = XMLClientHandler()
        self.hostServer = self.XML.getServerAddress()
        self.portServer = self.XML.getServerPort()
        self.username = None
        self.Log = Log(self.XML.getEnableLog())
        self.Chat = chat
        self.Message = Message(self.Log)
        self.Security = SecurityClient(self.XML.getSecurityServerKey())
        self.Log.log('Client initialized')

    #Functions to communicate with Server#
    def sendServer(self, text, id = None):
        """
            Send a message to the Server, containing the text passed as argument. With the
            passed id we can distinguish the security protocol that must be used, if it is None
            the encryption is not used

            :type text: String
            :param text: the string containing the message that must be sent to the server
            :type id: String
            :param id: the type of protocol that we must use. If 'rsa' we use RSA, 'aes' we use AES, None no encryption is used
            :rtype: int
            :return: If there is a problem with the communication -1, else return a number greater than 0
        """

        msg = ''
        if id is None:
            msg = text.encode('utf-8')

        elif id == 'rsa':
            text = text.encode(self.CODE_TYPE)
            msg = self.Security.RSAEncryptText(text, self.Security.serverPublicKey)
            #hash is None if the signature can not be done
            hash = self.Security.getSignature(text)
            if hash is None:
                hash = self.Security.getDigest(text)
            msg = msg+hash

        elif id == 'aes':
            text = text.encode(self.CODE_TYPE)
            msg = self.Security.AESEncryptText(text)

        ret = self.socketServer.send(msg)

        if ret == 0:
            #Socket is close
            self.Log.log('Problem in the communication with the server')
            #we try to reconnect to the Server
            if self.connectServer() == -1:
                self.logout()
                self.Log.log('It is not possible to reconnect with the server')
            return -1
        else:
            self.Log.log('Message sent to the Server')
            return ret

    def connectServer(self) :
        """
            Open the connection with the server creating the a new socket
            :rtype: int
            :return: if the connection has been set up in the correct way 1, else -1
        """

        try :
            self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketServer.settimeout(20)
            self.socketServer.connect((self.hostServer, self.portServer))
            self.Log.log('Connection established with the server')
            return 1
        except :
            #print('Connection refused by the server! Please try again later!')
            self.Log.log('Error in connection with the server, is it down?')
            return -1

    def loadWaitingMessages(self, msgs) :
        """
            Used only after the login is done correctly to handle all the waiting
            messages, msgs, in the server, those have been stored while the user was offline.
            All the messages are taken and putted in a structure containing all the
            messages related to the specific communication. The text of the message is encrypted with RSA of the sender.
            :type msgs: dict
            :param msgs: Contains the list of all the waiting messages in the server, each message is inside a dictionary
        """
        for x in msgs:
            ct = int(msgs[x]['Text']).to_bytes(256,byteorder='big')
            pt = self.Security.RSADecryptText(ct).decode(self.CODE_TYPE)
            self.Message.addMessagetoConversations(msgs[x]['Sender'], pt, msgs[x]['Time'], 1)

        self.Log.log('Loaded all the waiting messages')

    def receiveServer(self):
        """
            Receive and decrypt the messages from the server

            :rtype: Int or Dict
            :return: -1 if there is an error, 1 if the client asked for the waiting messages, otherwise the dictionary received from the server
        """
        try:
            ret = self.socketServer.recv(self.BUFFER_SIZE)
            if not ret:
                self.Log.log('Connection with the server closed!')
                return -1
            else:
                msg = self.Security.decryptServerMessage(ret)
                if msg is None:
                    print('The connection is not safe!')
                    self.onClosing()
                #print('secondo me è qua!')
                msg = msg.decode(self.CODE_TYPE)
                self.Log.log('Received a message from the SERVER: ' + msg)

                dictMsg = json.loads(msg)
                if dictMsg['id'].isdigit() :
                    if int(dictMsg['id']) > 0 :
                        self.Log.log('There are messages pending in the server')
                        self.loadWaitingMessages(dictMsg['messages'])
                    else :
                        self.Log.log('No messages stored in the server')
                    return 1
                else:
                    return dictMsg
                    #ELIMINARE SE FUNZIONA LA SEND_MESSAGE_OFFLINE
                    #if dictMsg['id'] == '.' :
                    #    return dictMsg['status']
                    #else :
        except:
            self.Log.log('An Exception has been raised in the receiveServer function')
            return -1

    #Functions for the FrontEnd#
    def register(self, username, password, name, surname, email):
        '''
            Start the Sign Up Protocol with the server in order to register, call the security
            to generate the Diffie-Hellman parameters, send the public parameters with the others
            to the server

            :type username: String
            :param username: the username
            :type password: String
            :param password: the password that will be obscured with an hash
            :type name: String
            :param name: the name of the user
            :typer surname: String
            :param surname: the surname of the user
            :type email: String
            :param email: the email of the user

            :rtype: Int
            :return: 1 if all has gone in the correct way, 0 if error in registration, -1 if security error in the communication
        '''

        msg = {}
        msg['id'] = '1'
        msg['user'] = username.lower()
        msg['password'] = password#str(int.from_bytes(self.Security.getDigest(password.encode(self.CODE_TYPE)), byteorder='big'))
        msg['name'] = name
        msg['surname'] = surname
        msg['email'] = email
        msg['clientNonce'] = self.Security.generateNonce(6)

        self.Log.log('Starting Sign Up Protocol')
        status = self.signUpProtocol(msg)

        if status == 1 :
            self.Log.log('Succesfully registered')
            if not self.Security.savePrivateKey(self.XML.getSecurityPath()+'-'+username + '.pem'):
                self.Log.log('Problem saving the private key of the client!')
            else:
                self.Log.log('Key saved Succesfully')

        else :
            #we can handle better the possible error
            self.Log.log('Error in registration. Status ' + str(status))

        self.Security.resetKeys()
        return status

    def signUpProtocol(self, msg):
        """
            Implements all the Sign Up Protocol in the client

            :type msgToSend: Dict
            :param msgToSend: content of the M1 message with the data of the user
            :rtype: Int
            :return: 1 if all has gone in the correct way, 0 if error in registration, -1 if security error in the communication
        """
        username = msg['user']
        msgToSend = json.dumps(msg)
        self.sendServer(msgToSend, 'rsa')

        self.Security.generate_key()
        key = self.Security.getSerializedPublicKey().decode('utf-8')
        self.sendServer(key)
        self.Log.log('Sent all M1')

        dict = self.receiveServer()
        self.Log.log('Received M2')

        status = int(dict['status'])
        if status != 1:
            self.Security.resetKeys()
            return status

        if dict['clientNonce'] != msg['clientNonce']:
            self.Log.log('The nonce received in M2 is not equal to mine. Connection not fresh!')
            self.Security.resetKeys()
            return -1

        msg = {}
        msg['serverNonce'] = dict['serverNonce']
        msg['g'],msg['p'] = self.Security.generateDHParameters()
        if self.Security.saveParameters(msg['g'], msg['p'], self.XML.getSecurityParameters()+'-'+username+'.'):
            self.Log.log('Succesfully saved the parameters')
        else:
            self.Log.log('Problems saving g and p')

        self.sendServer(json.dumps(msg), 'rsa')
        self.Log.log('Sent M3')
        ct = self.socketServer.recv(self.BUFFER_SIZE)
        self.Log.log('Received M4')
        pt = self.Security.decryptServerMessage(ct)

        if self.Security.getDigest(json.dumps(msg).encode(self.CODE_TYPE)) != pt:
            self.Security.resetKeys()
            self.Log.log('The digest received in M4 is not right!')
            return -1

        self.Log.log('Succesfully completed the Sign Up Protocol')
        return status

    def login(self, username, password):
        """
            Load the private key for he user specified, with the parameter username, then
            start the Authentication Protocol and perform the login for the user username
            with the password. The server will never see the real password but only the hash.
            If all is correct it makes start an instance of ConnectionHandler in order to
            handle the receiving connections for the peer to peer communication

            :type username: String
            :param username: the username
            :type password: String
            :param password: the password
            :rtype: Int
            :return: 1 of all is correct, 0 if the username or the password are wrong, -1 if the user is already connected with another device, -2 for security problems
        """
        self.username = username.lower()
        self.portp2p = random.randint(6001,60000)
        if not self.Security.initializeSecurity(self.XML.getSecurityPath(), self.username):
            return -2

        msg = {}
        msg['id'] = '2'
        msg['username'] = self.username
        msg['password'] = password#str(int.from_bytes(self.Security.getDigest(password.encode(self.CODE_TYPE)), byteorder='big'))
        msg['porta'] = str(self.portp2p)
        self.Security.addClientNonce(username, self.Security.generateNonce(12))
        msg['clientNonce'] = self.Security.getClientNonce(self.username)
        msgToSend = json.dumps(msg)

        self.Log.log('Starting the Authentication Protocol')
        value = self.authenticationProtocol(msgToSend)
        if value == 1:
            self.Log.log('Succesfull logged in as ' + self.username)
            #Load the local conversations
            self.Message.loadConversations(self.username)
            #Load the waiting messages stored in the server
            self.receiveServer()
            #starting the connectionHandler in order to manage the connections
            self.connectionHandler = ConnectionHandler(self.username, self.portp2p, self.Log, self.Chat, self.CODE_TYPE, self.Message, self.Security)
            self.connectionHandler.start()
        else:
            if value == 0 :
                self.Log.log('Login : Wrong Username or Password')
            elif value == -1 :
                self.Log.log('Login : You are already connected with another device')
            else:
                self.Log.log('Login : Security problem')
                self.logout()
            self.Security.resetKeys()
        return value

    def authenticationProtocol(self, msgToSend):
        """
            Implements all the Authentication Protocol

            :type msgToSend: Dict
            :param msgToSend: contain the information that goes inside M1
            :rtype: Int
            :return: 1 if all is correct, 0 if the username or the password are wrong, -1 if the user is already logged connected with another device, -2 for security problems
        """
        self.sendServer(msgToSend, 'rsa')
        self.Log.log('Sent M1')
        dict = self.receiveServer()
        self.Log.log('Received M2')

        if dict['clientNonce'] != self.Security.getClientNonce(self.username):
            self.Log.log('The nonce in M2 is not the expected one. Connection is not fresh for me!')
            return -2

        self.Security.AddServerSymmetricKey(dict['key'])
        if self.Security.loadDHParameters(self.XML.getSecurityParameters()):
            self.Log.log('Parameters correctly loaded')
        else:
            self.Log.log('Problems loading the parameters')

        msg = {}
        msg['serverNonce'] = dict['serverNonce']
        self.Security.serverNonce = msg['serverNonce']
        self.sendServer(json.dumps(msg), 'aes')
        self.Log.log('Sent M3')
        self.Log.log('Authentication Protocol completed correctly')
        return int(dict['status'])

    def startConnection(self, receiver):
        '''
            Ask to the server if a client, specified with the parameter receiver, is online: if it is
            then it starts the Online Key Exchange Protocol, else it performs the Offline Communication

            :type receiver: String
            :param receiver: the username of the client to contact
            :rtype: Int
            :return: 1 if all is correct and client is online, 0 if all is correct and client is offline, -1 login not done, -2 talking to yourself, -3 receiver does not exist, -4 security problem
        '''
        self.Log.log('Run of startConnection')
        if self.username == None:
            self.Log.log('User tries to contact someone without doing the login')
            return -1

        receiver = receiver.lower()
        msg = {}
        msg['id'] = '3'
        msg['username'] = receiver

        if msg['username'] == self.username:
            self.Log.log('User tries to contact itself')
            return -2

        msgToSend = json.dumps(msg)
        self.sendServer(msgToSend, 'aes')
        self.Log.log('Sent M1 of Online Key Exchange and Offline Communication')

        dict =  self.receiveServer()
        self.Log.log('received M2 of Online Key Exchange and Offline Communication')

        value = dict['status']
        msg = ''

        if value == '0' :
            self.Log.log('Communication offline with the user: ' + receiver)
            self.Security.insertKeyClient(receiver, dict['key'].encode('utf-8'))
            self.socketClient[receiver] = 'server'
            return 0
        elif value == '-1' :
            msg = 'Error: user does not have done the login'
        elif value == '-2' :
            msg = 'Error: you can not connect with yourself'
        elif value == '-3' :
            msg = 'Error: the contacted user does not exist'
        else :
            msgs = value.split(':')
            ip = msgs[0]
            port = msgs[1]
            msg = receiver + ' has IP:Port : ' + value
            self.Log.log('Starting a new connection with ' + receiver)
            self.socketClient[receiver] = socket.socket()
            try:

                self.socketClient[receiver].connect((ip, int(port)))
                self.Log.log('Continuing the Online Key Exchange Protocol')
                value = self.onlineKeyExchangeProtocol(receiver, dict)
            except:
                self.Log.log('Problem connecting with the other client, starting the offline communication')
                self.socketClient[receiver] = 'server'
                return 0

        self.Log.log('startConnection correctly concluded')
        return int(value)

    def onlineKeyExchangeProtocol(self, receiver, dict):
        """
            Implements the Online Key Exchange protocol
        """
        #info contains the symmetric message from the server to the client
        cipherText = dict['info'].to_bytes(dict['lenInfo'], byteorder='big')
        sign = self.Security.getSignature(cipherText)
        self.socketClient[receiver].send(cipherText+sign)

        if self.Security.isSymmetricKeyClientPresent(receiver):
            return 1

        self.Security.insertKeyClient(receiver, dict['key'].encode('utf-8'))

        self.Security.generateDH(dict['p'], dict['g'], receiver)
        plainText = self.Security.getSharedKey(receiver)
        pt1 = plainText[:round(len(plainText)/2)]
        pt2 = plainText[round(len(plainText)/2):]

        ct1 = self.Security.RSAEncryptText(pt1, self.Security.getKeyClient(receiver))
        sign1 = self.Security.getSignature(pt1)
        ct2 = self.Security.RSAEncryptText(pt2, self.Security.getKeyClient(receiver))
        sign2 = self.Security.getSignature(pt2)
        self.socketClient[receiver].send(ct1+sign1+ct2+sign2)

        print('sended all the M3 message')
        ############GETTING THE PUBLIC Y_B ##################
        msg = self.socketClient[receiver].recv(self.BUFFER_SIZE)
        msg1 = msg[:int(len(msg)/2)]
        msg2 = msg[int(len(msg)/2):]
        signature = msg1[-256:]
        msg = msg1[:-256]
        pt1 = self.Security.RSADecryptText(msg)
        if not self.Security.VerifySignature(pt1, signature, receiver):
            print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
            return -4
        else:
            print('integrity of the DH shared_key is valid')

        signature = msg2[-256:]
        msg = msg2[:-256]
        pt2 = self.Security.RSADecryptText(msg)
        if not self.Security.VerifySignature(pt2, signature, receiver):
            print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
            return -4
        else:
            print('integrity of the DH shared_key is valid')

        sharedKey = (pt1+pt2)
        print('YB è : ' + str(sharedKey))

        msg = self.socketClient[receiver].recv(self.BUFFER_SIZE)
        signature = msg[-256:]
        msg = msg[:-256]
        msg = self.Security.RSADecryptText(msg)
        dictBin = zlib.decompress(msg)
        if not self.Security.VerifySignature(dictBin, signature, receiver):
            print('The integrity is not valid for the sender. Signature:\n' + signature)
            return -4
        else:
            print('integrity of the DH shared_key is valid')
        dict = json.loads(dictBin)
        print('message M4 received ' + json.dumps(dict))
        print('starting computing key')
        self.Security.computeDHKey(receiver, sharedKey, 0)
        print('Computed key in the sender')
        ###############VERIFICA CHE IL NONCE SIA GIUSTO############
        ###TO DO TO DO TO DO TO DO TO DO TO DO TO DO TO DO TO DO###
        ###########################################################
        self.Security.addClientNonce(receiver, 0)

        Nb = dict['Nb']
        print('CRIPTATO CON AES ' + str(Nb))
        temp1 = Nb.to_bytes(dict['lenNb'], byteorder='big')
        temp2 = self.Security.AESDecryptText(temp1, receiver)
        #print(temp2)
        Nb = int.from_bytes(temp2, byteorder='big')
        self.Security.addClientNonce(receiver, Nb)
        print('Invio M5')
        Nb = self.Security.AESEncryptText(temp2, receiver)
        ret = self.socketClient[receiver].send(Nb)
        if ret == 0:
            msg = 'Error in sending the message to the client connection redirected to the server'
            self.socketClient[receiver] = 'server'
            return 0
        return 1


    def sendMessageOffline(self, receiver, text, time):
        '''
            Used to send and store a message in the server for an offline user
            The message is sent with the prefix '4|'
            if the message has been sent correctly return 1
            if there was an error in the db and the message has not been saved return 0
            otherwise return -1 for general errors
        '''
        msg = {}
        msg['id'] = '4'
        msg['Receiver'] = receiver
        t = self.Security.RSAEncryptText(text.encode(self.CODE_TYPE), self.Security.getKeyClient(receiver))
        #print(len(t))
        msg['Text'] = int.from_bytes(self.Security.RSAEncryptText(text.encode(self.CODE_TYPE), self.Security.getKeyClient(receiver)), byteorder='big')
        msg['Time'] = time
        msgToSend = json.dumps(msg)
        print('message sent to server')
        self.sendServer(msgToSend, 'aes')

        value = int(self.receiveServer()['status'])
        if value == 1:
            self.Log.log('Message send correctly to be stored in the Server')
        elif value == 0:
            self.Log.log('Error in the database! Try again later!')
        return value-1

    def sendClient(self, receiver, text, logout=None):
        '''
            Used to send a message [text] to the user [receiver]
            checks if there is an existing connection with the user [receiver]
            if not then it tries to create the p2p connection if not possible
            and the user exists then send the message to the server
            Handles the passage of the receiver from online to offline
        '''
        print('sendClient chiamata -> logout:')
        print(logout)
        if not receiver in self.socketClient.keys() or self.socketClient[receiver] == 'server' :
            value = self.startConnection(receiver)
            if value == 0 : #client offline
                self.socketClient[receiver] = 'server'
            elif value == 1 : #client online, connection established correctly
                self.Log.log('Connection established with ' + receiver)
                #self.socketClient[receiver].send(text.encode(self.CODE_TYPE))
            else :
                print('Client does not exist!!!')
                return value

        msg = self.Message.createMessageJson(text, str(datetime.datetime.now()), self.username, logout)
        if self.socketClient[receiver] == 'server' :
            #Check after x time if receiver is now online
            self.Message.addMessagetoConversations(receiver, text, str(datetime.datetime.now()), 0)
            return self.sendMessageOffline(receiver, text, str(datetime.datetime.now()))
        else :
            try:
                #value = self.socketClient[receiver].send(str(len(msg)).encode(self.CODE_TYPE))
                #print('sended ' + str(len(msg)))
                self.Log.log('Message to be send : ' + msg)
                pt = msg.encode(self.CODE_TYPE)
                print('Cripto il messaggio da inviare con AES')
                ct = self.Security.AESEncryptText(pt, receiver)
                #ct = pt
                value = self.socketClient[receiver].send(ct)
                print('message sended to client')
                if value > 0:
                    self.Message.addMessagetoConversations(receiver, text, str(datetime.datetime.now()), 0)
                    return 1
                else :
                    raise ConnectionResetError()
            except:
                self.Log.log(receiver + 'has disconnected')
                self.Security.resetSymmetricKeyClient(receiver)
                #possible signal to FrontEnd
                self.socketClient[receiver] = 'server'
                return self.sendClient(receiver, text)

    def setAutoLogin(self, remember, username, password):
        self.XML.setAutoLogin(remember, username, password)

    def checkAutoLogin(self):
        if not self.XML.getRemember():
            return -2
        else :
            self.username = self.XML.getUserName()
            return self.login(self.username, self.XML.getUserPwd())

    def logout(self, ordinatedUserList = None):
        msg = {}
        msg['id'] = '0'
        self.sendServer(json.dumps(msg), 'aes')
        print(self.socketClient.keys())
        for x in self.socketClient.keys() :
            print(x)
            if not self.socketClient[x] == 'server' :
                self.sendClient(x, 'logout', 1)
                self.socketClient[x].shutdown(socket.SHUT_RDWR)
                self.socketClient[x].close()
        if self.username is not None:
            self.Message.saveConversations(self.username, ordinatedUserList)
        self.username = None
        self.Security = SecurityClient(self.XML.getSecurityServerKey())
        self.connectionHandler.stop()
        self.connectionHandler = None

    def onClosing(self, ordinatedUserList = None): #clean up before close
        #close the socket connection
        self.XML.saveXML()
        if ordinatedUserList is not None :
            self.logout(ordinatedUserList)
        try:
            self.socketServer.shutdown(socket.SHUT_RDWR)
            self.socketServer.close()
        except:
            os._exit(0)
        print('Exiting....')
        os._exit(0)
