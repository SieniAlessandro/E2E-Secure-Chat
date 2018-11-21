from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, cmac
from cryptography.exceptions import InvalidSignature
from cryptography.exceptions import InvalidTag
import os

class Security:
    def __init__(self,path,BackupPath):
        """
            Initialize the security module loading,using the path passed as argument,if present the private and public key,
            otherwise generating and saving it

            :type path: String
            :param path: The path of the pem file in which the private key must be written
            :type backupPath: String
            :param backupPath: The path of the pem file in which the private key must be written
        """
        try:
            with open(path,"rb") as pem:
                try:
                    self.privateKey = serialization.load_pem_private_key(pem.read(),password=b'ServerMPSprivatekey',backend=default_backend())
                    self.publicKey = self.privateKey.public_key()
                except ValueError:
                    try:
                        with open(BackupPath,"rb") as backup:
                            print("The key is corrupted but i have the backup")
                            backup_key = serialization.load_pem_private_key(backup.read(),password=b'ServerMPSprivatekey',backend=default_backend())
                            with open(path,"wb") as pem_write:
                                self.privateKey = backup_key
                                self.publicKey = self.privateKey.public_key()
                                serializedPrivateKey = backup_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(b'ServerMPSprivatekey'))
                                pem_write.write(serializedPrivateKey)
                    except FileNotFoundError:
                        print("I don't have the backup,and the key is corrupted")
                        self.generate_key(path,BackupPath)
        except FileNotFoundError:
            try:
                with open(BackupPath,"rb") as backup,open (path,"wb") as pem:
                    print("I don't have the private key but i have the backup")
                    try:
                        backup_key = serialization.load_pem_private_key(backup.read(),password=b'ServerMPSprivatekey',backend=default_backend())
                        SerializedPrivateKey = backup_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(b'ServerMPSprivatekey'))
                        self.privateKey = backup_key
                        self.publicKey = self.privateKey.public_key()
                        pem.write(SerializedPrivateKey)
                    except ValueError:
                        print("The backup is corrupted")
                        self.generate_key(path,BackupPath)
            except FileNotFoundError:
                print("I don't have anything")
                with open(path,"wb") as pem, open(BackupPath,"wb") as backup:
                    self.generate_key(path,BackupPath)

    def generate_key(self,path,backupPath):
        """
            Generate and write the private key

            :type path: String
            :param path: The path of the pem file in which the private key must be written
            :type backupPath: String
            :param backupPath: The path of the pem file in which the private key must be written
        """
        with open(path,"wb") as pem, open(backupPath,"wb") as backup:
            self.privateKey = rsa.generate_private_key(public_exponent=65537,\
                                                   key_size=8196,\
                                                   backend=default_backend())
            self.publicKey = self.privateKey.public_key()
            serializedPrivateKey = self.privateKey.private_bytes(encoding=serialization.Encoding.PEM,
                                                             format=serialization.PrivateFormat.PKCS8,
                                                             encryption_algorithm=serialization.BestAvailableEncryption(b'ServerMPSprivatekey'))
            pem.write(serializedPrivateKey)
            backup.write(serializedPrivateKey)

    def RSAEncryptText(self,text):
        """
            Encrypt the text using RSA with the public key of the handled client

            :type text: Bytes
            :param text: The plain text that must be encrypted
            :rtype: Bytes
            :return: cipherText: the cipher text relative to the plain text passed as argument
        """

        cipherText = self.ClientPublicKey.encrypt(text,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None
                                                         )
                                            )
        return cipherText

    def RSADecryptText(self,cipherText):
        """
            Decrypt the message using your own private key

            :type cipherText: Bytes
            :param cipherText: The cipher text that must be decrypted
            :rtype: Bytes
            :param plaintext: the plain text obtained by decriptying the plain text passed as argument
        """

        plaintext = self.privateKey.decrypt(cipherText,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None
                                                         )
                                            )
        return plaintext

    def splitMessage(self,data,len):
        """
            Split the message in two part, usefull when you need to compare a message with a digest or a signature

            :type data: Bytes
            :param data: The Data that must be divided in two parts
            :type len: Int
            :param len: The point in which the list must be divided
            :rtype: <Bytes,Bytes>
            :return: The touple of lists obtained by dividing in two part the original data :
        """
        return [data[0:len*(-1)],data[len*(-1):]]

    def generateDigest(self,data):
        """
            Generate the digest of the message (in bytes) using SHA-256

            :type data: Bytes
            :param data: The data of which we want generate the digest
            :rtype: Bytes
            :return: The digest of the data passed as argument
        """"
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def getSignature(self,data):
        """ Generate a signature by the private key
            Parameter:
                    text: the data we want to sign                          : Bytes
            Return:
                    signature: the signature of the data passed as argument : Bytes  """
        signature = self.privateKey.sign(data,
                                     padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                 salt_length=padding.PSS.MAX_LENGTH
                                                 ),
                                     hashes.SHA256()
                                     )
        return signature

    def VerifySignature(self,data,signature):
        """ Verify if the signature,generated by the private key of the client,is associated to the data
            Parameter:
                    data        : The data we want to verify    : Bytes
                    signature   : The signature used to check   : Bytes
            Return:
                    True        : The signature is correct      : Boolean
                    False       : The signature is not correct  : Boolean   """
        try:
            self.ClientPublicKey.verify(signature,data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
            return True
        except InvalidSignature:
            return False

    def AddClientKey(self,key):
        """
            Add the public key of the client, in order to use them when it is necessary to encrypt using RSA, pass the key encoded by 'utf-8'

            :type key: Bytes
            :param key: The public key of the client we want to add
        """
        self.ClientPublicKey = serialization.load_pem_public_key(key,backend=default_backend())

    def getSerializedPublicKey(self):
        """
            Get the server public key serializable (it must be decoded) in order to get it printable and sendable

            :rtype: Bytes
            :return: The public key of the client
        """
        return self.publicKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def getSerializedClientPublicKey(self):
        """
            Get the server public key serializable (it must be decoded) in order to get it printable and sendable

            :rtype: Bytes
            :return: The public key of the client
        """
        return self.ClientPublicKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def generateSymmetricKey(self,len,nonce):
        """
            Generate a symmetric key used in AESGCM with a lenght (suggested 192/256 bit ) and pass a nonce used with the key
            to cipher a text (each operation has its own couple of <key,nonce> in order to guarantee security)

            :type len: Int
            :param len: The lenght of the symmetric key (in bit)
            :type nonce: Int
            :param nonce: The nonce used to encrypt/decrypt
            :rtype: Int
            :return: The operations are done correctly
        """

        self.nonce  = nonce
        self.len = len
        self.SymmetricKey = AESGCM.generate_key(bit_length=self.len);
        return 0

    def getSymmetricKey(self):
        """
            Get the symmetric key as bytes, if you want to serialize it you have to transform it (suggested in integer with a number of
            intger nessary = bit_length of key / 8, becaues each integer reppresent a byte)

            :rtype: Bytes
            :return: The symmetric key used to encrypt/decrypt
        """
        return self.SymmetricKey

    def AddPacketNonce(self,nonce):
        """
            Add the nonce used in the AES when is necessary to encapsulate some information about the starter of the conversation
            between two user

            :type nonce : Int
            :param nonce: The nonce used to encrypt the packets necessary to exchange key from two clients
        """
        self.packetNonce = nonce

    def AESDecryptText(self,ct):
        """
            Cipher text with AES and GCM in order to guarantee autenthicity and integrity of the message, the handling of the nonce
            is provided by the function itself (each encyption/decryption must increment the nonce in order to maintain it always
            synchronized on the two side )

            :type ct: Bytes
            :param ct: The cipher text to decrypt
            :rtype: Bytes or None
            :return: The plain text obtained by decrypting the cipher text passed as parameter
        """
        try:
            aescgm = AESGCM(self.SymmetricKey)
            self.nonce = self.nonce+1
            pt = aescgm.decrypt(self.nonce.to_bytes(16,byteorder='big'),ct,None)
            return pt
        except:
            print("Error in decrypt with AESCGM")
            return None

    def AESEncryptText(self,pt):
        """
            Cipher text with AES and GCM in order to guarantee autenthicity and integrity of the message, the handling of the nonce
            is provided by the function itself (each encyption/decryption must increment the nonce in order to maintain it always
            synchronized on the two side )

            :type pt: Bytes
            :param pt: The plain text to encrypt
            :type ct: Bytes or None
            :param ct:  The cipher text obtained by encrypting the plain text passed as argument
        """
        try:
            aesgcm = AESGCM(self.SymmetricKey)
            self.nonce = self.nonce + 1
            return aesgcm.encrypt(self.nonce.to_bytes(16,byteorder='big'), pt, None)
        except:
            print("Error in encrypt GCM")
            return None

    def PacketAESEncryptText(self,pt):
        """
            Cipher text with AES and a special nonce (sended by the client during the login procedure) in order
            to encapsulate some information useful for the exchange of key between two online user

            :type pt: Bytes
            :param pt: The plain text to encrypt
            :rtype: Bytes or None
            :return: The cipher text obtained by encrypting the plain text passed as argument
        """
        try:
            aesgcm = AESGCM(self.SymmetricKey)
            self.packetNonce = self.packetNonce + 1
            print("Nonce per il pacchetto : "+str(self.packetNonce))
            return aesgcm.encrypt(self.packetNonce.to_bytes(16,byteorder='big'), pt, None)
        except:
            print("Error in encrypt GCM")
            return None

    def addDHparameters(self,p,g):
        """
            Add the DH parameter, in orde to retrieve efficiently when necessary
            :type p: Int
            :param p: the Diffie Hellman P parameter
            :type g: Int
            :param g: The Diffie Hellman G parameter
        """
        self.p = p
        self.g = g

    def getDHparameters(self):
        """
            Get the DH parameters as a list [p,g]

            :rtype: [Int,Int]
            :return: The tuple composed by the two DH parameters
        """
        return [self.p,self.g]

    def generateNonce(self,size):
        """
            Generate a nonce of a dimension chosed (in bytes) a get it as an Integer encoded in Big Endian

            :type size: Int
            :param size:The size (in Bytes) of the nonce
            :rtype: Int
            :return: A nonce generated using the system call specific for cryptography purpose of the dimensione passed as argument
        """
        return int.from_bytes(os.urandom(size),byteorder='big')
