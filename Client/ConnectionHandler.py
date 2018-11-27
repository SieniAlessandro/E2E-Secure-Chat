import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *
import zlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class ConnectionHandler(Thread) :
    BUFFER_SIZE = 2048
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
        try:
            self.socketListener.bind((self.ip,portp2p))
        except OSError:
            print('eat')
        self.Log = Log
        self.Chat = Chat
        self.Code = Code
        self.Message = Message
        self.Security = Security
        self.Log.log('MessageHandler Initialized! Associated port: ' + str(self.portp2p))
        self.sizeNonce = 6
    '''
        Handle the connection with a specific user
        when a message is received is passed to the FrontEnd (AMEDEO)
        If the connection is closed the Thread return -1 after sending a signal
        to the front end
    '''
    def receiveMessage(self, conn) :
        #self.Log.log('Connection started with ' + str(user))
        messageFromServer = conn.recv(self.BUFFER_SIZE)
        msg = messageFromServer[:-256]

        #print('P2P connection: ' + str(len(msg)))
        #print('len msg ' + str(len(messageFromServer)))
        #ct = int.from_bytes(msg, byteorder='big')
        signature = messageFromServer[-256:]
        #Decrypt the symmetric message from the server to retreìeve
        text = self.Security.AESDecryptText(msg, self.username, 1)
        if text is None:
            print('Error in AES')
            return
        dict = json.loads(text)
        peerUsername = dict['username']
        ret = self.Security.insertKeyClient(peerUsername, dict['key'])
        if not self.Security.VerifySignature(msg, signature, peerUsername):
            print('The integrity is not valid for the receiver. Signature:\n' + str(signature))

            return

        #print('messaggio del server visto con successo!')
        if not self.Security.isSymmetricKeyClientPresent(peerUsername):
            msg = conn.recv(self.BUFFER_SIZE)
            msg1 = msg[:int(len(msg)/2)]
            msg2 = msg[int(len(msg)/2):]
            signature = msg1[-256:]
            msg = msg1[:-256]
            pt1 = self.Security.RSADecryptText(msg)
            if not self.Security.VerifySignature(pt1, signature, peerUsername):
                print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
                return
            else:
                print('integrity of the DH shared_key is valid')

            signature = msg2[-256:]
            msg = msg2[:-256]
            pt2 = self.Security.RSADecryptText(msg)
            if not self.Security.VerifySignature(pt2, signature, peerUsername):
                print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
                return
            else:
                print('integrity of the DH shared_key is valid')

            sharedKey = (pt1+pt2)
            #print('YA è : ' + str(sharedKey))

            self.Security.computeDHKey(peerUsername, sharedKey,1)
            #print('KEY COMPUTED!!!')

            plainText = self.Security.getSharedKey(self.username)
            pt1 = plainText[:round(len(plainText)/2)]
            pt2 = plainText[round(len(plainText)/2):]

            ct1 = self.Security.RSAEncryptText(pt1, self.Security.getKeyClient(peerUsername))
            sign1 = self.Security.getSignature(pt1)
            ct2 = self.Security.RSAEncryptText(pt2, self.Security.getKeyClient(peerUsername))
            sign2 = self.Security.getSignature(pt2)

            conn.send(ct1+sign1+ct2+sign2)

            #print('sended all mine Y')
            plainText = {}
            #        plainText['sharedKey'] = int.from_bytes(self.Security.getSharedKey(self.username), byteorder='big')
            plainText['Nsa'] = dict['Nsa']
            Nb = self.Security.generateNonce(self.sizeNonce)
            self.Security.addClientNonce(peerUsername,0)

            NbAES = self.Security.AESEncryptText(Nb.to_bytes(self.sizeNonce,byteorder='big'), peerUsername)
            plainText['lenNb'] = len(NbAES)
            plainText['Nb'] = int.from_bytes(NbAES, byteorder='big')
            #print('CRIPTATO CON AES:' + str(plainText['Nb']))
            self.Security.addClientNonce(peerUsername,Nb)
            ptBit = json.dumps(plainText).encode(self.Code)

            ptBitCompress = zlib.compress(ptBit)

            #print('Lunghezza messaggio M4: ' + str(len(ptBitCompress)))
            cipherText = self.Security.RSAEncryptText(ptBitCompress, serialization.load_pem_public_key(dict['key'].encode('utf-8'), backend=default_backend()))
            sign = self.Security.getSignature(ptBit)
            #print('message prepared properly')
            conn.send(cipherText+sign)
            #print('message M4 sended to ' + peerUsername)

            msg = conn.recv(self.BUFFER_SIZE)
            plainText = int.from_bytes(self.Security.AESDecryptText(msg, peerUsername), byteorder='big')
            if Nb == plainText:
                print('Nb da usare ' + str(Nb))
                print('the connection has been set up in the correct way')
            else:
                print('Mio Nb: ' + str(Nb))
                print('Ricevuto Nb: ' + str(plainText))
                return

############################################################
        while True:
            try:
                ct = conn.recv(self.BUFFER_SIZE)
                if not ct :
                    raise Exception()

                pt = self.Security.AESDecryptText(ct, peerUsername)
                #pt = ct
                msg = pt.decode(self.Code)

                #print('Message received: ' + msg + ' length : ' + length)
                dict = json.loads(msg)

                self.Log.log(dict['sender'] + ' send : ' + msg)
                if self.Chat is not None:
                    self.Chat.notify(dict['sender'], dict['text'], dict['time'], False, False)
                #appendToConversation
                self.Message.addMessagetoConversations(dict['sender'], dict['text'], dict['time'], 1)
            except Exception as e:
                #print(e)
                self.Security.resetSymmetricKeyClient(peerUsername)
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
            conn.settimeout(60)
            self.Log.log('Accepted a new connecion')
            t = Thread(target=self.receiveMessage, args=(conn, ))
            t.start()
