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
    def __init__(self,path,BackupPath,publicKey = None):
        if publicKey is None:
            self.ServerInitialized(path,BackupPath)
        else:
            self.AddClientKey(publicKey)
    def ServerInitialized(self,path,BackupPath):
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
        cipherText = self.ClientPublicKey.encrypt(text,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None
                                                         )
                                            )
        return cipherText

    def RSADecryptText(self,cipherText):
        plaintext = self.privateKey.decrypt(cipherText,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None
                                                         )
                                            )
        return plaintext

    def splitMessage(self,pt,len):
        return [pt[0:len*(-1)],pt[len*(-1):]]

    def generateDigest(self,pt):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(pt)
        return digest.finalize()

    def getSignature(self,text):
        signature = self.privateKey.sign(text,
                                     padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                 salt_length=padding.PSS.MAX_LENGTH
                                                 ),
                                     hashes.SHA256()
                                     )
        return signature

    def VerifySignature(self,text,signature):
        try:
            self.ClientPublicKey.verify(signature,text,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
            return True
        except InvalidSignature:
            return False

    def AddClientKey(self,key):
        self.ClientPublicKey = serialization.load_pem_public_key(key,backend=default_backend())

    def getSerializedPublicKey(self):
        return self.publicKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def generateSymmetricKey(self,len,nonce):
        self.nonce  = nonce
        self.len = len
        self.SymmetricKey = AESGCM.generate_key(bit_length=self.len);
        return 0

    def getSymmetricKey(self):
        return self.SymmetricKey;

    def getSymmetricKeyasDict(self):
        key = {}
        key["lenght"] = str(self.len)
        key["content"] = [byte for byte in self.SymmetricKey]
        return key

    def AddSymmetricKeyFromDict(self,dict):
        """Must be passed as argument the dict located at message['key']"""
        self.len = int(key["lenght"])
        self.SymmetricKey = struct.pack("B"*int(dict["lenght"]/8),*dict["content"])

    def AESDecryptText(self,ct):
        try:
            aescgm = AESGCM(self.SymmetricKey)
            self.nonce = self.nonce+1
            print("Decrypt:"+str(self.nonce))
            pt = aescgm.decrypt(self.nonce.to_bytes(16,byteorder='big'),ct,None)
            return pt
        except:
            print("Error in decrypt with AESCGM")
            return None

    def AESEncryptText(self,pt):
        try:
            aesgcm = AESGCM(self.SymmetricKey)
            self.nonce = self.nonce + 1
            print("Encrypt:"+str(self.nonce))
            return aesgcm.encrypt(self.nonce.to_bytes(16,byteorder='big'), pt, None)
        except:
            print("Error in encrypt GCM")
            return None

    def addDHparameters(self,p,g):
        self.p = p
        self.g = g

    def getDHparameters(self):
        return [self.p,self.g]

    def generateNonce(self,size):
        return int.from_bytes(os.urandom(size),byteorder='little')
