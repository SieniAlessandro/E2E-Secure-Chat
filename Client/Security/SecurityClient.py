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
        """
        self.username = username
        path += '-' + username + '.pem'

        try:
            with open(path,"rb") as pem:
                try:
                    self.privateKey = serialization.load_pem_private_key(pem.read(),password=b'keyClients',backend=default_backend())
                    self.publicKey = self.privateKey.public_key()
                    self.clientKeys[username] = self.publicKey
                except ValueError:
                    print('utente non ha più la chiave privata')
        except FileNotFoundError:
            print('chiave persa')

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
        except Exception as e:
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

    def AESDecryptText(self,cipherText,username = None, nonce = None):
        """
            Decrypt the passed cipherText with AES, if the nonce is not None, then
            uses the symmetricKey to send a message to the server, if there is a specified
            username then it uses the nonce of the client because the message is been received
            from the server for the Online Key Exchange Protocol, else it uses the nonce with the
            server. If there is a specified nonce then it uses the symmetricKey of the client passed
            as username and the nonce passed

            :type cipherText: Bytes
            :param cipherText: the cipher text that must be decrypted
            :type username: String or None
            :param username: None if we have to use the symmetric key of the server

        """
        try:
            if nonce is not None:
                #decrypt with the symmetric key with the server
                aescgm = AESGCM(self.SymmetricKey)
                if username is None:
                    self.serverNonce = self.serverNonce+1
                    return aescgm.decrypt(self.serverNonce.to_bytes(16, byteorder="big"),cipherText,None)
                else:
                    self.clientNonce[username] = self.clientNonce[username]+1
                    return aescgm.decrypt(self.clientNonce[username].to_bytes(16, byteorder="big"),cipherText,None)
            else:
                #decrypt with the symmetric key with the client - username
                aescgm = AESGCM(self.clientSymmetricKeys[username])
                self.clientNonce[username] = self.clientNonce[username]+1
                print('decripto con AES , nonce '+ str(self.clientNonce[username]))
                return aescgm.decrypt(self.clientNonce[username].to_bytes(16, byteorder="big"),cipherText,None)
        except TypeError as t:
            print(t)
            print("Error in decrypt GCM")
            return None
        except:
            print(sys.exc_info()[0])
            raise Exception()

    def AESEncryptText(self,pt, username = None):
        #try:
        if username is None:
            #print(self.serverNonce)
            aesgcm = AESGCM(self.SymmetricKey)
            self.serverNonce = self.serverNonce+1
            #print('encryptnonce ' + str(self.serverNonce))
            return aesgcm.encrypt(self.serverNonce.to_bytes(16, byteorder="big"), pt, None)
        else:
            aesgcm = AESGCM(self.clientSymmetricKeys[username])
            self.clientNonce[username] = self.clientNonce[username]+1
            print('Nonce client used for AES encrypt ' + str(self.clientNonce[username]))
            #print('encryptnonce ' + str(self.serverNonce))
            return aesgcm.encrypt(self.clientNonce[username].to_bytes(16, byteorder="big"), pt, None)
        #except Exception as e:
        #    print(e)
        #    print("Error in encrypt GCM")
        #    return None

    def decryptText(self, text):
        msg = b''
        if self.SymmetricKey is None:
            #print(len(text[0:-1025]))
            sign = text[-1025:]
            msg = self.RSADecryptText(text[0:-1025])
            if self.VerifySignature(msg, sign):
                return msg
            else:
                None
        else:
            return self.AESDecryptText(text, None, 1)


    def savePrivateKey(self, path):
        with open(path,"wb") as pem:
            print("saving the keys")
            serializedPrivateKey = self.privateKey.private_bytes(
                                            encoding=serialization.Encoding.PEM,
                                            format=serialization.PrivateFormat.PKCS8,
                                            encryption_algorithm =serialization.BestAvailableEncryption(
                                                b'keyClients'
                                                )
                                            )
            pem.write(serializedPrivateKey)

    '''
        Methods to establish a secure communication client to client
        using Diffie-Hellman
    '''
    def generateDHParameters(self):
        '''
        generates the parameters g and p, these are public and can be reused
        '''
        print('generate parameters')
        self.parameters = dh.generate_parameters(
                                            generator=2,
                                            key_size=512,
                                            backend=default_backend()
                                            )
        self.parnum = self.parameters.parameter_numbers()
        print('g: ' + str(self.parnum.g) + ' p:' + str(self.parnum.p))
        return [self.parnum.g, self.parnum.p]

    def saveParameters(self,g,p, path):
        txt = {}
        txt['g'] = g
        txt['p'] = p
        with open(path+'json', 'w') as parameters:
            json.dump(txt, parameters)

    def loadParameters(self, path):
        par = {}
        with open(path+'-'+self.username+'.json', 'r') as parameters:
            par = json.loads(parameters.read())
        self.generateDH(par['p'], par['g'], self.username)

    def resetKeys(self):
        self.privateKey = None
        self.publicKey = None
        self.DHPrivateKey = {}
        self.clientKeys = {}
        self.clientSymmetricKeys = {}
        self.SymmetricKey = None
        self.serverNonce = None
        self.clientNonce = {}

    def generateDH(self, p, g, user):
        print('generateDH: parameters p, g and user:\np= ' +str(p) +'\ng= ' + str(g) + '\nuser= ' + str(user))
        pn = dh.DHParameterNumbers(int(p), int(g))
        self.parameters = pn.parameters(default_backend())
        #publicNumbers = self.parameters.DHPublicNumbers()
        self.DHPrivateKey[user] = self.parameters.generate_private_key()


#    def computeDHtoSend(self, user):
#        return self.DHPrivateKey[user]
    def getSharedKey(self, user):

        y = self.DHPrivateKey[user].public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        print('the public key to send [y]')
        print(y)
        return y

    def computeDHKey(self, user, shared_key, mine=None):
        '''
            We must pass the value g^b mod p = shared_key received by the other client
            and compute the key as (g^b mod p)^a mod p
            when we compute this we remove from the system
        '''
        print('key of the communication with the other host has been computed')
        y = ''
        if mine is None:
            y = self.DHPrivateKey[user].exchange(serialization.load_pem_public_key(shared_key,backend=default_backend()))
        else:
            y = self.DHPrivateKey[self.username].exchange(serialization.load_pem_public_key(shared_key,backend=default_backend()))

        self.clientSymmetricKeys[user] = HKDF(
                 algorithm=hashes.SHA256(),
                 length=32,
                 salt=None,
                 info=b'handshake data',
                 backend=default_backend()
            ).derive(y)
        print('This is it:')
        print(self.clientSymmetricKeys[user])


    def insertKeyClient(self, user, key):
        #print('inserting the key of ' + user)
        #print(key)
        self.clientKeys[user] = serialization.load_pem_public_key(key.encode('utf-8'),backend=default_backend())

    def resetSymmetricKeyClient(self, user):
        try:
            del self.clientSymmetricKeys[user]
        except:
            print()

    def isSymmetricKeyClientPresent(self,user):
        try:
            return self.clientSymmetricKeys[user] is not None
        except:
            return False

    def getKeyClient(self, user):
        return self.clientKeys[user]

    def addClientNonce(self, user, nonce):
        self.clientNonce[user] = nonce

    def getClientNonce(self, user):
        return self.clientNonce[user]

    def generateNonce(self,size):
        """ Generate a nonce of a dimension chosed (in bytes) a get it as an Integer encoded in Big Endian
            Parameter:
                    size: The size (in Bytes) of the nonce                                                                          : int
            Return:
                    A nonce generated using the system call specific for cryptography purpose of the dimensione passed as argument  : int """
        return int.from_bytes(os.urandom(size),byteorder='big')
