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
    '''
    Back end of the client
    '''
    BUFFER_SIZE = 2048*1024
    PORT_SERVER = 6000
    HOST_SERVER = '10.102.12.15'#'127.0.0.1'
    CODE_TYPE = 'utf-8'
    socketClient = {}

    def __init__(self, chat = None):
        self.XML = XMLClientHandler()
        self.hostServer = '127.0.0.1'#self.XML.getServerAddress()#self.HOST_SERVER #IPv4 Address of the server
        self.portServer = self.XML.getServerPort()
        self.portp2p = random.randint(6001,60000)
        self.username = None
        self.Log = Log()
        self.Log.log('Client initialized')
        self.Chat = chat
        self.Message = Message(self.Log)
        self.Security = SecurityClient(self.XML.getSecurityServerKey())
        #################TESTING####################
        #self.Security.generateDHParameters()
        #Thread(target=self.Security.generate_key()).start()
        ############################################
        #print(self.Security.getServerPublicKey().decode('utf-8'))
    #Functions to communicate with Server#
    def sendServer(self, text, id = None):
        '''
        Send a Message, containing the parameter text, to the Server
        encoded with utf-8
        If the communication with the server is closed return -1
        else return the return of the send function [a number > 0]
        '''

        textBit = ''
        hash = ''
        if id is 'register':
            textBit = text.encode('utf-8')#self.CODE_TYPE)
            #print(str(len(textBit)))
        elif id == 'server':
            text = text.encode(self.CODE_TYPE)
            textBit = self.Security.RSAEncryptText(text, self.Security.serverPublicKey)
            #print('len mes crypted: ' + str(len(textBit)))
            hash = self.Security.getSignature(text)
            if hash is None:
                h = hashes.Hash(hashes.SHA256(), backend=default_backend())
                h.update(text)
                hash = h.finalize()

            textBit = textBit+hash
        else:
            text = text.encode(self.CODE_TYPE)
            textBit = self.Security.AESEncryptText(text)

        ret = self.socketServer.send(textBit)

        if ret == 0:
            #Socket is close
            self.Log.log('Problem in the connection with the server')
            return -1
        else:
            #self.Log.log('Message: <' + text + '> sended to the server correctly')
            return ret

    def connectServer(self) :
        '''
            Open the connection with the server creating the socket [socketServer]
            if the connection goes wrong the function return -1 otherwise 1
        '''

        try :
            self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketServer.connect((self.hostServer, self.portServer))
            return 1
        except :
            print('Connection refused by the server! Please try again later!')
            self.Log.log('Error in connection with the server, is it down?')
            return -1

    def retrieveMessage(self, msgs) :
        '''
            Used, after the Login is done correctly, to retrieve all the waiting
            messages in the server sended to me from other users while I was offline
            All the messages are taken and putted in a structure containing all the
            messages related to the specific connection with that specific user
            TO FINISH
        '''
        #print(msgs)
        for x in msgs:
            ct = int(msgs[x]['Text']).to_bytes(256,byteorder='big')
            pt = self.Security.RSADecryptText(ct).decode(self.CODE_TYPE)
            self.Log.log('sender :' + msgs[x]['Sender'])
            self.Log.log('text : ' + pt)
            self.Log.log('time : ' + msgs[x]['Time'])
            self.Message.addMessagetoConversations(msgs[x]['Sender'], pt, msgs[x]['Time'], 1)

    def receiveServer(self):
        '''
            Receive Messages from the server
            if the socket is closed or there is an exception return -1
            otherwise it returns a specific value depending on the message received
            by the server
        '''
        try:
            ret = self.socketServer.recv(self.BUFFER_SIZE)
            if not ret:
                self.Log.log('Connection with the server closed!')
                return -1
            else:
                msg = self.Security.decryptText(ret)
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
                        self.retrieveMessage(dictMsg['messages'])
                    else :
                        self.Log.log('No messages stored in the server')
                    return 1
                else:
                    #if ! we are waiting to know the IP of the host we want to connect to
                    if dictMsg['id'] == '!' :
                        return dictMsg
                        #if ? we are waiting to know if the login is done
                    elif dictMsg['id'] == '?' :
                        return dictMsg
                        #if - we are waiting to know how the registration is done
                    elif dictMsg['id'] == '-' :
                        return dictMsg
                        #if . we are waiting to know if a message sended to be stored
                        #in the server has been succesfully received and stored
                    elif dictMsg['id'] == '.' :
                        return dictMsg['status']
                    else :
                        print('The protocol for this kind of message has not been implemented yet')
                        return dictMsg['id']
        except Exception as e:
            print(e)
            self.Log.log('An Exception has been raised in the receiveServer function')
            return -1
        except:
            print(sys.exc_info()[0])
            self.Log.log('An Exception has been raised in the receiveServer function')
            return -1
    ######################################

    #Functions for the FrontEnd#
    def register(self, username, password, name, surname, email, key = 0):
        '''
            send a message to the server to register
            The message is sent with the prefix '1|'
            if succesfull registration return 1
            otherwise return 0 {we can use other codes to know why it is not okay}
        '''

        msg = {}
        msg['id'] = '1'
        msg['user'] = username.lower()
        msg['password'] = password
        msg['name'] = name
        msg['surname'] = surname
        msg['email'] = email
        clientNonce = int(binascii.hexlify(os.urandom(6)),16)
        msg['clientNonce'] = clientNonce
        #msg['key'] = self.Security.getSerializedPublicKey().decode('utf-8')
        msgToSend = json.dumps(msg)
        print('inizio registrazione')
        self.sendServer(msgToSend, 'server')
        #print(str(msgToSend) + ' \nlen :' + str(len(msgToSend)))

        self.Security.generate_key()

        #print(len(self.Security.getSerializedPublicKey().decode('utf-8')))
        #print(self.Security.getSerializedPublicKey().decode('utf-8'))
        key = self.Security.getSerializedPublicKey().decode('utf-8')
        self.sendServer(key, 'register')

        dict = self.receiveServer()
        #print(dict)
        status = int(dict['status'])
        if status != 1:
            self.Security.resetKeys()
            return status

        if dict['clientNonce'] != clientNonce:
            print('The connection is not fresh for me')
            return 0

        msg = {}
        g,p = self.Security.generateDHParameters()
        msg['serverNonce'] = dict['serverNonce']
        msg['g'] = g
        msg['p'] = p

        self.sendServer(json.dumps(msg), 'server')

        res = self.socketServer.recv(self.BUFFER_SIZE)
        res = self.Security.decryptText(res)

        if self.Security.getDigest(json.dumps(msg).encode(self.CODE_TYPE)) != res:
            print('the digest is not right!')
            self.onClosing()

        if status == 1 :
            self.Log.log('Succesfully registered')
            self.Security.savePrivateKey(self.XML.getSecurityPath()+'-'+username + '.pem', self.XML.getSecurityBackup()+'-'+username+'.pem', password)
        else :
            #we can handle better the possible error
            self.Log.log('Error in registration')

        self.Security.saveParameters(g, p, self.XML.getSecurityParameters()+'-'+username+'.')
        self.Security.resetKeys()
        return status


    def login(self, username, password):
        '''
            Used to do the login -> creates an attribute to know the username [username]
            Send a message to the server with the prefix '2|'
            If all it's correct return 1
            if the username or password are wrong return 0
            if the host is already connected with another device return -1
        '''
        self.username = username.lower()


        msg = {}
        msg['id'] = '2'
        msg['username'] = self.username
        msg['password'] = password
        msg['porta'] = str(self.portp2p)
        self.Security.addClientNonce(username, self.Security.generateNonce(12))
        msg['clientNonce'] = self.Security.getClientNonce(self.username)
        msgToSend = json.dumps(msg)
        self.Security.initializeSecurity(self.XML.getSecurityPath(), self.XML.getSecurityBackup(), self.username, password.encode(self.CODE_TYPE))
        self.sendServer(msgToSend, 'server')

        dict = self.receiveServer()
        #print('the dict is ' + json.dumps(dict))
        if dict['clientNonce'] != self.Security.getClientNonce(self.username):
            print('the connection is not fresh for me!')
            self.onClosing()

        self.Security.AddSymmetricKeyFromDict(dict['key'])
        self.Security.loadParameters(self.XML.getSecurityParameters())

        msg = {}
        msg['serverNonce'] = dict['serverNonce']
        self.Security.serverNonce = msg['serverNonce']
        self.sendServer(json.dumps(msg), self.Security.getSymmetricKey())
        #print('message sent with AES')
        value = int(dict['status'])
        if value == 1 :
            self.Log.log('Succesfull logged in as ' + self.username)

            self.Message.loadConversations(self.username)
            #wating to know if there are waiting messages on the server
            self.receiveServer()
            #starting the connectionHandler in order to manage
            #connections received from new clients
            ch = ConnectionHandler(self.username, self.portp2p, self.Log, self.Chat, self.CODE_TYPE, self.Message, self.Security)
            ch.start()
        else:
            if value == 0 :
                self.Log.log('Login : Wrong Username or Password')
            elif value == -1 :
                self.Log.log('Login : You are already connected with another device')
            else:
                self.Log.log('Login : an unreachable part of the code has been reached, yupee!!! value: ' + value)
            self.Security.resetKeys()
        return value

    def startConnection(self, receiver):
        '''
        Start a new connection with the user [receiver]:
            The message is sent with the prefix '3|'
            if it is online and all goes in the correct way then return 1
            -> creates the new socket with the receiver [socketClient[receiver]]
            else if receiver is offline return 0
                 if you do not have done the login return -1
                 if you are trying to talk to yourself return -2
                 if the receiver does not exist -3
                 if an exception has been raised -4
        '''
        msg = {}
        msg['id'] = '3'
        msg['username'] = receiver.lower()
        msgToSend = json.dumps(msg)
        self.sendServer(msgToSend)

        dict =  self.receiveServer()
        #print('message received from the server : ' + json.dumps(dict))
        value = dict['status']
        msg = ''

        if value == '0' :
            msg = 'user offline'
            self.Security.insertKeyClient(receiver, dict['key'])
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
            msg = receiver.lower() + ' has IP:Port : ' + value
            self.Log.log('Starting a new connection with ' + receiver.lower())


            self.socketClient[receiver] = socket.socket()
            ret = self.socketClient[receiver].connect((ip, int(port)))
            #info contains the symmetric message from the server to the client
            cipherText = dict['info'].to_bytes(dict['lenInfo'], byteorder='big')
            sign = self.Security.getSignature(cipherText)
            self.socketClient[receiver].send(cipherText+sign)
            print('sended symmetric message')

            self.Security.insertKeyClient(receiver, dict['key'])

            self.Security.generateDH(dict['p'], dict['g'], receiver)
            plainText = self.Security.getSharedKey(receiver)
            pt1 = plainText[:round(len(plainText)/2)]
            pt2 = plainText[round(len(plainText)/2):]

            ct1 = self.Security.RSAEncryptText(pt1, self.Security.getKeyClient(receiver))
            sign = self.Security.getSignature(pt1)
            self.socketClient[receiver].send(ct1+sign)

            ct2 = self.Security.RSAEncryptText(pt2, self.Security.getKeyClient(receiver))
            sign = self.Security.getSignature(pt2)
            self.socketClient[receiver].send(ct2+sign)
            print('sended all the M3 message')
            ############GETTING THE PUBLIC Y_B ##################
            msg = self.socketClient[receiver].recv(self.BUFFER_SIZE)
            signature = msg[-256:]
            msg = msg[:-256]
            pt1 = self.Security.RSADecryptText(msg)
            if not self.Security.VerifySignature(pt1, signature, receiver):
                print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
                return
            else:
                print('integrity of the DH shared_key is valid')

            msg = self.socketClient[receiver].recv(self.BUFFER_SIZE)
            signature = msg[-256:]
            msg = msg[:-256]
            pt2 = self.Security.RSADecryptText(msg)
            if not self.Security.VerifySignature(pt2, signature, receiver):
                print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
                return
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
                return
            else:
                print('integrity of the DH shared_key is valid')
            dict = json.loads(dictBin)
            print('message M4 received ' + json.dumps(dict))
            print('starting computing key')
            self.Security.computeDHKey(receiver, sharedKey)
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
            self.socketClient[receiver].send(self.Security.AESEncryptText(temp2, receiver))

            print('STARTCONNECTION CONCLUSA???????')
            value = 1
            if ret == 0:
                msg = 'Error in sending the message to the client connection redirected to the server'
                self.socketClient[receiver] = 'server'
            else:
                self.Log.log('An exception has been raised in the startConnection function')
                return -4
        self.Log.log(msg)
        return int(value)

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
        self.sendServer(msgToSend)

        value = int(self.receiveServer())
        if value == 1:
            self.Log.log('Message send correctly to be stored in the Server')
        elif value == 0:
            self.Log.log('Error in the database! Try again later!')
        return value-1

    def sendClient(self, receiver, text):
        '''
            Used to send a message [text] to the user [receiver]
            checks if there is an existing connection with the user [receiver]
            if not then it tries to create the p2p connection if not possible
            and the user exists then send the message to the server
            Handles the passage of the receiver from online to offline
        '''
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

        msg = self.Message.createMessageJson(text, str(datetime.datetime.now()), self.username)
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
                ct = self.Security.AESEncryptText(pt, receiver)
                value = self.socketClient[receiver].send(ct)

                if value > 0:
                    self.Message.addMessagetoConversations(receiver, text, str(datetime.datetime.now()), 0)
                    return 1
                else :
                    raise ConnectionResetError()
            except ConnectionResetError:
                self.Log.log(receiver + 'has disconnected')
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

    def logout(self, ordinatedUserList):
        for x in self.socketClient :
            if not isinstance(x, str) :
                x.shutdown(socket.SHUT_RDWR)
                x.close()
        self.Message.saveConversations(self.username, ordinatedUserList)
        msg = {}
        msg['id'] = '0'
        self.sendServer(json.dumps(msg))
        self.username = None


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
