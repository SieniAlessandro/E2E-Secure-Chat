import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *
import zlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class ConnectionHandler(Thread) :
    """
        Handles all the connection received from the other peers and handles all
        the packets received from them
    """
    BUFFER_SIZE = 2048
    #Constructor
    def __init__(self, username, portp2p, Log, Chat, Message, Security) :
        """
            Creates a new socket and binds it to the port destinated for the connections p2p

            :type username: String
            :param username: the local user
            :type portp2p: Int
            :param portp2p: the port used for the p2p connections
            :type Log: Log
            :param Log: the log
            :type Chat: ChatList
            :param Chat: used to insert the messages in the front end of the client
            :type Message: Message
            :param Message: the Message handler
            :type Security: SecurityClient
            :param Security: handles the Security for the client
        """
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
        self.Message = Message
        self.Security = Security
        self.sizeNonce = 6
        self.Log.log('MessageHandler Initialized! Associated port: ' + str(self.portp2p))
    def receiveMessage(self, conn) :
        """
            Handle the connection with a the user connected to the socket passed as param conn.
            Call the Online Key Exchange Protocol as the peer receiving the connection
            :type conn: Socket
            :param conn: the socket used for the communication with the peer
        """
        peerUsername = self.onlineKeyExchangeProtocolReceiver()
        if not isString(peerUsername):
            self.Log.log('Error in the Security Protocol')
            return

        try:
            #Chiedi ad AMEDEO
            self.Chat.chatListDict[peerUsername][1].updateState(1)
        except:
            print()

        while True:
            try:
                cipherText = conn.recv(self.BUFFER_SIZE)
                if not cipherText :
                    raise Exception()
                plainText = self.Security.AESDecryptText(cipherText, peerUsername)

                msg = plainText.decode('utf-8')

                dict = json.loads(msg)

                if dict['logout']:
                    self.Log.log('received the logout message from ' + peerUsername)
                    self.Chat.chatListDict[peerUsername][1].updateState(0)
                    self.Security.resetSymmetricKeyClient(peerUsername)
                    return

                self.Log.log(peerUsername + ' send : ' + msg)
                #Create the notification for this chat on the GUI
                self.Chat.notify(dict['sender'], dict['text'], dict['time'], False, False)
                #appendToConversation
                self.Message.addMessagetoConversations(dict['sender'], dict['text'], dict['time'], 1)

            except Exception as e:
                self.Security.resetSymmetricKeyClient(peerUsername)
                self.Log.log('Connection closed')
                return

    def onlineKeyExchangeProtocolReceiver(self):
        """
            Implements the Online Key Exchange Protocol for the receiver peer

            :rtype: String or Int
            :return: the username of the peer with which the conneciton has been established or an error code
        """
        messageFromServer = conn.recv(self.BUFFER_SIZE)
        msg = messageFromServer[:-256]
        #signature of the server is composed by 256 bytes
        signature = messageFromServer[-256:]
        #Decrypt the symmetric message from the server to retreìeve
        text = self.Security.AESDecryptText(msg, self.username, 1)
        if text is None:
            self.Log.log('Error in AES')
            return -1
        dict = json.loads(text)
        peerUsername = dict['username']
        ret = self.Security.insertKeyClient(peerUsername, dict['key'].encode('utf-8'))
        if not self.Security.VerifySignature(msg, signature, peerUsername):
            self.Log.log('The integrity is not valid for the receiver. Signature:\n' + str(signature))
            return -2

        #print('messaggio del server visto con successo!')
        if not self.Security.isSymmetricKeyClientPresent(peerUsername):
            msg = conn.recv(self.BUFFER_SIZE)
            msg1 = msg[:int(len(msg)/2)]
            msg2 = msg[int(len(msg)/2):]
            signature = msg1[-256:]
            msg = msg1[:-256]
            plainText1 = self.Security.RSADecryptText(msg)
            if not self.Security.VerifySignature(plainText1, signature, peerUsername):
                print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
                return
            else:
                print('integrity of the DH shared_key is valid')

            signature = msg2[-256:]
            msg = msg2[:-256]
            plainText2 = self.Security.RSADecryptText(msg)
            if not self.Security.VerifySignature(plainText2, signature, peerUsername):
                print('The integrity is not valid for the receiver. Signature:\n' + str(signature))
                return
            else:
                print('integrity of the DH shared_key is valid')

            sharedKey = (plainText1+plainText2)
            #print('YA è : ' + str(sharedKey))

            self.Security.computeDHKey(peerUsername, sharedKey,1)
            #print('KEY COMPUTED!!!')

            plainText = self.Security.getSharedKey(self.username)
            plainText1 = plainText[:round(len(plainText)/2)]
            plainText2 = plainText[round(len(plainText)/2):]

            cipherText1 = self.Security.RSAEncryptText(plainText1, self.Security.getKeyClient(peerUsername))
            sign1 = self.Security.getSignature(plainText1)
            cipherText2 = self.Security.RSAEncryptText(plainText2, self.Security.getKeyClient(peerUsername))
            sign2 = self.Security.getSignature(plainText2)

            conn.send(cipherText1+sign1+cipherText2+sign2)

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
            plainTextBit = json.dumps(plainText).encode('utf-8')

            plainTextBitCompress = zlib.compress(plainTextBit)

            #print('Lunghezza messaggio M4: ' + str(len(ptBitCompress)))
            cipherText = self.Security.RSAEncryptText(plainTextBitCompress, serialization.load_pem_public_key(dict['key'].encode('utf-8'), backend=default_backend()))
            sign = self.Security.getSignature(plainTextBit)
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

        return peerUsername

    '''
        In a loop accept new connection with other clients
        and starts a new thread that will handle the single connection
        {this is done in order to distinguish the single connection
         with the specific user}
    '''
    def run(self) :
        try:
            while True:
                self.socketListener.listen(50)
                (conn, (ip,port)) = self.socketListener.accept()
                conn.settimeout(60)
                self.Log.log('Accepted a new connecion')
                t = Thread(target=self.receiveMessage, args=(conn, ))
                t.start()

        except:
            self.Log.log('Connection Handler has been closed')
            self.socketListener.close()
            return -1

    def stop(self) :
        self.socketListener.close()
