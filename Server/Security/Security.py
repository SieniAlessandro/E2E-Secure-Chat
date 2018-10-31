from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Security:
    def __init__(self,path,BackupPath):
        self.ServerInitialized(path,BackupPath)
    def ServerInitialized(self,path,BackupPath):

            try:
                with open(path,"rb") as pem:
                    try:
                        self.private_key = serialization.load_pem_private_key(pem.read(),password=b'ServerMPSprivatekey',backend=default_backend())
                        self.publicKey = self.private_key.public_key()
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
                            generate_key(path,BackupPath)
                except FileNotFoundError:
                    print("I don't have anything")
                    with open(path,"wb") as pem, open(BackupPath,"wb") as backup:
                        self.generate_key(path,backupPath)
    def generate_key(self,path,backupPath):
        with open(path,"wb") as pem, open(backupPath,"wb") as backup:
            self.privateKey = rsa.generate_private_key(public_exponent=65537,\
                                                   key_size=4098,\
                                                   backend=default_backend())
            self.publicKey = self.private_key.public_key()
            serializedPrivateKey = private_key.private_bytes(encoding=serialization.Encoding.PEM,
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
        plaintext = self.privateKey.decrypt(ciphertext,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None
                                                         )
                                            )
        return plaintext
    def getSignature(self,text):
        signature = private_key.sign(text,
                                     padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                 salt_length=padding.PSS.MAX_LENGTH
                                                 ),
                                     hashes.SHA256()
                                     )
        return signature
    def VerifySignature(self,text,signature):
        try:
            self.publicKey.verify(signature,message,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
            return True
        except InvalidSignature:
            return False
    def AddClientKey(self,key):
        self.ClientPublicKey = key
    
