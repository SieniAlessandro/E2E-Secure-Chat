from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Security:
    def __init__(self,type,path,BackupPath):
        if type == 1:
            self.ServerInitialized(path,BackupPath)
        else:
            print("Not else implemented for the client PEM")


    def ServerInitialized(self,path,BackupPath):
            try:
                with open(path,"rb") as pem:
                    try:
                        private_key = serialization.load_pem_private_key(pem.read(),password=b'ServerMPSprivatekey',backend=default_backend())
                    except ValueError:
                        try:
                            with open(BackupPath,"rb") as backup:
                                print("The key is corrupted but i have the backup")
                                backup_key = serialization.load_pem_private_key(backup.read(),password=b'ServerMPSprivatekey',backend=default_backend())
                                with open(path,"wb") as pem_write:
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
                            pem.write(SerializedPrivateKey)
                        except ValueError:
                            print("The backup is corrupted")
                except FileNotFoundError:
                    print("I don't have anything")
                    with open(path,"wb") as pem, open(BackupPath,"wb") as backup:
                        self.generate_key(path,backupPath)
                        
    def generate_key(self,path,backupPath):
        with open(path,"wb") as pem, open(backupPath,"wb") as backup:
            private_key = rsa.generate_private_key(public_exponent=65537,\
                                                   key_size=4098,\
                                                   backend=default_backend())
            serializedPrivateKey = private_key.private_bytes(encoding=serialization.Encoding.PEM,\
                                                             format=serialization.PrivateFormat.PKCS8,\
                                                             encryption_algorithm=serialization.BestAvailableEncryption(b'ServerMPSprivatekey'))
            pem.write(serializedPrivateKey)
            backup.write(serializedPrivateKey)
