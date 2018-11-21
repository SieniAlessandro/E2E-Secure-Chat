import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *


class ConnectionHandler(Thread) :
    MSG_LEN = 2048
    #Constructor
    '''
        Create a new socket and bind it to the port destinated for connectio p2p
    '''
    def __init__(self, username, portp2p, Log, Chat, Code, Message, Security) :
        Thread.__init__(self)
        self.ip = "0.0.0.0"
        self.username = username
        self.portp2p = portp2p
        self.users = []
        self.socketListener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socketListener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socketListener.bind((self.ip,portp2p))
        self.Log = Log
        self.Chat = Chat
        self.Code = Code
        self.Message = Message
        self.Security = Security
        self.Log.log('MessageHandler Initialized! Associated port: ' + str(self.portp2p))

    '''
        Handle the connection with a specific user
        when a message is received is passed to the FrontEnd (AMEDEO)
        If the connection is closed the Thread return -1 after sending a signal
        to the front end
    '''
    def receiveMessage(self, conn) :
        #self.Log.log('Connection started with ' + str(user))
        messageFromServer = conn.recv(self.MSG_LEN)
        msg = messageFromServer[:-256]

        print('P2P connection: ' + str(len(msg)))
        print('len msg ' + str(len(messageFromServer)))
        #ct = int.from_bytes(msg, byteorder='big')
        signature = messageFromServer[-256:]
        #Decrypt the symmetric message from the server to retreìeve
        text = self.Security.AESDecryptText(msg, self.username, 1)
        if text is None:
            print('Error in AES')
            return
        dict = json.loads(text)
        self.Security.insertKeyClient(dict['username'], dict['key'])
        if not self.Security.VerifySignature(msg, signature, dict['username']):
            print('The integrity is not valid for the receiver. Signature:\n' + str(signature))

            return

        print('messaggio del server visto con successo!')

        msg = conn.recv(self.MSG_LEN)
        signature = msg[-256:]
        msg = msg[:-256]
        pt = self.Security.RSADecryptText(msg)
        if not self.Security.VerifySignature(pt, signature, dict['username']):
            print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
            return
        else:
            print('integrity of the DH shared_key is valid')

        sharedKey = self.Security.RSADecryptText(msg)

        self.Security.computeDHKey(self.username, sharedKey)
        print('KEY COMPUTED!!!')

        plainText = {}
        plainText['sharedKey'] = self.Security.getSharedKey(dict['username'])
        plainText['Nsa'] = dict['Nsa']
        Nb = self.Security.generateNonce(6)
        self.Security.addClientNonce(dict['username'],0)

        plaintext['Nb'] = self.Security.AESEncryptText(Nb.to_bytes(6,byteorder='big'), dict['username'])

        self.Security.addClientNonce(Nb,0)
        ptBit = json.dumps(plainText).encode(self.Code)
        cipherText = self.Security.RSAEncryptText(ptBit, self.Security.getKeyClient(dict['username']))
        sign = self.Security.getSignature(ptBit)

        conn.send(cipherText+sign)
        print('message sended to ' + dict['username'])

        msg = conn.recv(self.MSG_LEN)
        plainText = self.Security.AESDecryptText(msg, dict['username'])
        if Nb == plainText:
            print('the connection has been set up in the correct way')
        else:
            print('NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
            return

############################################################
        while True:
            try:
                msg = conn.recv(self.MSG_LEN)
                if not msg :
                    raise Exception()

                msg = msg.decode(self.Code)

                #print('Message received: ' + msg + ' length : ' + length)
                dict = json.loads(msg)

                self.Log.log(dict['sender'] + ' send : ' + msg)
                if self.Chat is not None:
                    self.Chat.notify(dict['sender'], dict['text'], dict['time'], False, False)
                #appendToConversation
                self.Message.addMessagetoConversations(dict['sender'], dict['text'], dict['time'], 1)
            except Exception as e:
                #print(e)
                self.Log.log('Connection closed')
                return -1
    '''
        In a loop accept new connection with other clients
        and starts a new thread that will handle the single connection
        {this is done in order to distinguish the single connection
         with the specific user}
    '''
    def run(self) :
        while True :
            self.socketListener.listen(50)
            (conn, (ip,port)) = self.socketListener.accept()
            self.Log.log('Accepted a new connecion')
            t = Thread(target=self.receiveMessage, args=(conn, ))
            t.start()
