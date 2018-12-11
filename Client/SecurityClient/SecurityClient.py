from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature
from cryptography.exceptions import InvalidTag
import json
import sys
import os

class SecurityClient:
    def __init__(self, serverPublicKeyPath):
        """
            Initialize the security module loading the server public key using the path passed as argument

            :type serverPublicKeyPath: String
            :param serverPublicKeyPath: The path of the pem file where the public key of the server is
        """
        self.privateKey = None
        self.publicKey = None
        self.DHPrivateKey = {}
        self.clientKeys = {}
        self.clientSymmetricKeys = {}
        self.SymmetricKey = None
        self.serverNonce = None
        self.clientNonce = {}
        with open(serverPublicKeyPath, 'rb') as pubfile:
            self.serverPublicKey = serialization.load_pem_public_key(pubfile.read(),backend=default_backend())

    #Communication with server
    def initializeSecurity(self,path, username):
        """
            Loads the private key of the user that is performing the login, using the path and the username passed as argument

            :type path: String
            :param path: The path of the pem file where the private key of the user is
            :type username: String
            :param username: The username of the user that is trying to login
            :rtype: Boolean
            :return: True if the key is loaded Succesfully, False if there is some problem
        """
        self.username = username
        path += '-' + username + '.pem'

        try:
            with open(path,"rb") as pem:
                self.privateKey = serialization.load_pem_private_key(pem.read(),password=b'keyClients',backend=default_backend())
                self.publicKey = self.privateKey.public_key()
                self.clientKeys[username] = self.publicKey
                return True
        except FileNotFoundError:
            print('chiave persa')
            return False

    def generate_key(self):
        """
            Creates the private key for the client
        """
        self.privateKey = rsa.generate_private_key(public_exponent=65537,\
                                               key_size=2048,\
                                               backend=default_backend())
        self.publicKey = self.privateKey.public_key()

    def RSAEncryptText(self,text, key):
        """
            Encrypt the text passed with the passed key

            :type text: Bytes
            :param text: the text that must be encrypted
            :type key: Bytes
            :param key: the key that must be used for encrypt with RSA
            :rtype: Bytes
            :return: the encrypted text
        """
        cipherText = key.encrypt(text,
                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                             algorithm=hashes.SHA256(),
                                             label=None
                                             )
                                 )
        return cipherText

    def getDigest(self,text):
        """
            Apply the hash to the text passed

            :type text: Bytes
            :param text: the text
            :rtype: Bytes
            :return: The digest
        """
        h = hashes.Hash(hashes.SHA256(), backend=default_backend())
        h.update(text)
        return h.finalize()

    def RSADecryptText(self,cipherText):
        """
            Perform the decryption of the passed cipherText with the private key
            of the client

            :type cipherText: Bytes
            :param cipherText: The cipher text
            :rtype: Bytes
            :return: The plain text
        """
        plaintext = self.privateKey.decrypt(cipherText,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None
                                                         )
                                            )
        return plaintext

    def getSignature(self,text):
        """
            Sign the passed text with the private key of the client

            :type text: Bytes
            :param text: The text that must be signed
            :rtype: Bytes
            :return: the signature
        """
        try:
            signature = self.privateKey.sign(text,
                                         padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                     salt_length=padding.PSS.MAX_LENGTH
                                                     ),
                                         hashes.SHA256()
                                         )
            return signature
        except:
            return None

    def VerifySignature(self,text,signature, user=None):
        """
            Performs the validation of the passed signature on the passed text using
            the public key of the server if the user is None, else uses the public key
            of the passed user

            :type text: Bytes
            :param text: the text to check the signature
            :type signature: Bytes
            :param signature: the signature that must be verify
            :type user: String or None
            :param user: The username of the user that had signed the text, if it's None the signature is of the server
            :rtype: Boolean
            :return: True if the signature is valide, else False
        """
        try:
            if user is None:
                self.serverPublicKey.verify(signature,text,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
            else:
                self.clientKeys[user].verify(signature,text,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
            return True
        except InvalidSignature as e:
            return False

    def getServerPublicKey(self):
        """
            Used to get the public key of the server

            :rtype: Bytes
            :return: The public key of the server
        """
        return self.serverPublicKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def getSerializedPublicKey(self):
        """
            Used to get the public key of the client

            :rtype: Bytes
            :return: The public key of the client
        """
        return self.publicKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def AddServerSymmetricKey(self,key):
        """
            Add the symmetric key for the conversation with the server
            :type key: Int
            :param key: the symmetric key
        """
        self.SymmetricKey = key.to_bytes(16, byteorder='big')

    def getSymmetricKey(self):
        """
            obtain the symmetricKey of the conversation with the server

            :rtype: Bytes
            :return: The symmetric key
        """
        return self.SymmetricKey;

    def AESDecryptText(self,cipherText,username = None, serverCommunication = None):
        """
            Decrypt the passed cipherText with AES, if the serverCommunication is not None, then
            uses the symmetricKey to send a message to the server, if there is a specified
            username then it uses the nonce of the client because the message is been received
            from the server for the Online Key Exchange Protocol, else it uses the nonce with the
            server. If there is a specified nonce then it uses the symmetricKey of the client passed
            as username and the nonce passed

            :type cipherText: Bytes
            :param cipherText: the cipher text that must be decrypted
            :type username: String or None
            :param username: None if we have to use the symmetric key of the server
            :type serverCommunication: Int or None
            :param serverCommunication: specify if the message will go to the server or to a client
        """
        if serverCommunication is not None:
            #decrypt with the symmetric key with the server
            aescgm = AESGCM(self.SymmetricKey)
            if username is None:
                #use the nonce created by the server
                self.serverNonce = self.serverNonce+1
                return aescgm.decrypt(self.serverNonce.to_bytes(16, byteorder="big"),cipherText,None)
            else:
                #use the nonce created by itself
                self.clientNonce[username] = self.clientNonce[username]+1
                return aescgm.decrypt(self.clientNonce[username].to_bytes(16, byteorder="big"),cipherText,None)
        else:
            #decrypt with the symmetric key of the conversation with the client - username
            aescgm = AESGCM(self.clientSymmetricKeys[username])
            #use the nonce generated during the online key exchange protocol
            self.clientNonce[username] = self.clientNonce[username]+1
            return aescgm.decrypt(self.clientNonce[username].to_bytes(16, byteorder="big"),cipherText,None)

    def AESEncryptText(self,plainText, user = None):
        """
            Encrypt the plain text passed using AES Galois Counter Mode. The nonce used
            is, if the username is None, the one of the server, else is the associated nonce
            with the user passed as parameter; the nonce is incremented every time in order
            to not use more than one time one the same value for the nonce.

            :type plainText: Bytes
            :param plainText: the text that must be encrypted
            :type user: String or None
            :param user: Specify which nonce must be used
            :rtype: Bytes
            :return: The encrypted message
        """
        if user is None:
            aesgcm = AESGCM(self.SymmetricKey)
            self.serverNonce = self.serverNonce+1
            return aesgcm.encrypt(self.serverNonce.to_bytes(16, byteorder="big"), plainText, None)
        else:
            aesgcm = AESGCM(self.clientSymmetricKeys[user])
            self.clientNonce[user] = self.clientNonce[user]+1
            return aesgcm.encrypt(self.clientNonce[user].to_bytes(16, byteorder="big"), plainText, None)

    def decryptServerMessage(self, cipherText):
        """
            Handles the decryption of the messages received from the Server, if
            the symmetric key with the server does not exist then uses RSA else
            AES is used

            :type cipherText: Bytes
            :param cipherText: The text that must decrypted
            :rtype: Bytes or None
            :return: The plain text or, if the signature is not valid, None
        """
        if self.SymmetricKey is None:
            #the signature length of the server is 1024
            sign = cipherText[-1025:]
            plainText = self.RSADecryptText(cipherText[0:-1025])
            if self.VerifySignature(plainText, sign):
                return plainText
            else:
                None
        else:
            return self.AESDecryptText(cipherText, None, 1)


    def savePrivateKey(self, path):
        """
            Save the Private Key of the client in a file in the specified param path

            :type path: String
            :param path: The specific path of the file where the key must be saved
            :rtype: Boolean
            :return: True if the key has been saved, otherwise False
        """
        try:
            with open(path,"wb") as pem:
                serializedPrivateKey = self.privateKey.private_bytes(
                                                encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm =serialization.BestAvailableEncryption(
                                                    b'keyClients'
                                                    )
                                                )
                pem.write(serializedPrivateKey)
                return True
        except:
            return False

    def generateDHParameters(self):
        """
            Generates the public parameters g and p for the diffie-hellman protocol
            :rtype: List<Int>
            :return: g and p in a list
        """
        self.parameters = dh.generate_parameters(
                                            generator=2,
                                            key_size=512,
                                            backend=default_backend()
                                            )
        self.parnum = self.parameters.parameter_numbers()
        return [self.parnum.g, self.parnum.p]

    def saveParameters(self,g,p, path):
        """
            Save the diffie-hellman public parameters g and p in a json file,
            these can be reused more than once

            :type g: Int
            :param g: the parameter g of diffie-hellman
            :type p: Int
            :param p: the parameter p of diffie-hellman
            :type path: String
            :param path: the path of the file where the parameters will be saved
            :rtype: Boolean
            :return: True if the save was done succesfully, False if it was not
        """
        txt = {}
        txt['g'] = g
        txt['p'] = p
        try:
            with open(path+'json', 'w') as parameters:
                json.dump(txt, parameters)
            return True
        except:
            return False

    def loadDHParameters(self, path):
        """
            Loads the diffie-hellman parameters g and p from the json file specified by path
            and starts the instance of the structure used to perform the diffie-hellman protocol

            :type path: String
            :param path: Path for the json file
            :rtype: Boolean
            :return: True if correctly loaded, False otherwise
        """
        par = {}
        try:
            with open(path+'-'+self.username+'.json', 'r') as parameters:
                par = json.loads(parameters.read())
        except:
            return False
        #self.username because this values will be used for all the received connections
        self.generateDH(par['p'], par['g'], self.username)
        return True


    def resetKeys(self):
        """
            Reset all the keys and nonce stored
        """
        self.privateKey = None
        self.publicKey = None
        self.DHPrivateKey = {}
        self.clientKeys = {}
        self.clientSymmetricKeys = {}
        self.SymmetricKey = None
        self.serverNonce = None
        self.clientNonce = {}

    def generateDH(self, p, g, user):
        """
            Generates a structure used for the Diffie-Hellman protcol, in
            paricular it is generate the unknown random value used to create the
            public value that must be sent to other peers and to compute the
            shared key, user specifies who is the owner of the parameters g and p

            :type p: Int
            :param p: parameter p of diffie-hellman
            :type g: Int
            :param g: parameter g of diffie-hellman
            :type user: String
            :param user: the owner of p and g
        """
        pn = dh.DHParameterNumbers(int(p), int(g))
        self.parameters = pn.parameters(default_backend())
        self.DHPrivateKey[user] = self.parameters.generate_private_key()

    def getSharedKey(self, user):
        """
            Used to get the shared key used in the conversation with the passed user

            :type user: String
            :param user: the username
            :rtype: Bytes
            :return: the shared symmetric key with the user
        """
        return self.DHPrivateKey[user].public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def computeDHKey(self, user, sharedKey, mine):
        """
            Generates the symmetric key for the conversation with the user, if mine is None
            this means that the parameters diffie-hellman used have been generated by the specified user,
            otherwise they are mine

            :type user: String
            :param user: user with which the conversation is active
            :type sharedKey: Bytes
            :param sharedKey: the public value sent by the user to complete the protocol
            :type mine: Boolean
            :param mine: Specified who has created the public parameters for diffie hellman
        """
        y = ''
        if not mine:
            y = self.DHPrivateKey[user].exchange(serialization.load_pem_public_key(sharedKey,backend=default_backend()))
        else:
            y = self.DHPrivateKey[self.username].exchange(serialization.load_pem_public_key(sharedKey,backend=default_backend()))

        self.clientSymmetricKeys[user] = HKDF(
                 algorithm=hashes.SHA256(),
                 length=32,
                 salt=None,
                 info=b'handshake data',
                 backend=default_backend()
            ).derive(y)

    def insertKeyClient(self, user, publicKey):
        """
            insert the public key of the user passed as parameter

            :type user: String
            :param user: the owner of the public key
            :type publicKey: Bytes
            :param publicKey: the public key of the user
        """
        self.clientKeys[user] = serialization.load_pem_public_key(publicKey,backend=default_backend())

    def resetSymmetricKeyClient(self, user):
        """
            Delete the symmetric key of the conversation with the passed user

            :type user: String
            :param user: the user relative to the symmetric key
        """
        try:
            if user in self.clientSymmetricKeys:
                del self.clientSymmetricKeys[user]
        except:
            print()

    def isSymmetricKeyClientPresent(self,user):
        """
            Check if exists a symmetric key for the conversation with the passed user

            :type user: String
            :param user: the user relative to the symmetric key
            :rtype: Boolean
            :return: True if the symmetric key is present, False otherwise
        """
        try:
            return self.clientSymmetricKeys[user] is not None
        except:
            return False

    def getKeyClient(self, user):
        """
            obtain the public key of the passed user

            :type user: String
            :param user: the owner of the public key required
            :rtype: Bytes
            :return: the public key of user
        """
        return self.clientKeys[user]

    def addClientNonce(self, user, nonce):
        """
            Used to add the passed nonce to a dictionary indexed with the corrispective user

            :type user: String
            :param user: the username correlated to that specific nonce
            :type nonce: Int
            :param nonce: the nonce used for the conversation with user
        """
        self.clientNonce[user] = nonce

    def getClientNonce(self, user):
        """
            obtain the nonce correlated with the passed user

            :type user: String
            :param user: used to obtain the correlated nonce
            :rtype: Int
            :return: nonce of the conversation with user
        """
        return self.clientNonce[user]

    def generateNonce(self,size):
        """
            Generate a nonce of a dimension chosed (in bytes) a get it as an Integer encoded in Big Endian

            :type size: Int
            :param size: The size (in Bytes) of the nonce
            :rtype: Int
            :return: A nonce generated using the system call specific for cryptography purpose of the dimensione passed as argument
        """
        return int.from_bytes(os.urandom(size),byteorder='big')
