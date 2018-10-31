from Security.Security import Security

class User:
    def __init__(self,_socket,_ip,_ClientPort,_ServerPort,_UserName):
        self.Ip = _ip
        self.ClientPort = _ClientPort
        self.ServerPort = _ServerPort
        self.Username = _UserName
        self.Socket = _socket
    def getUserName(self):
        return self.Username
    def getIp(self):
        return self.Ip
    def getServerPort(self):
        return self.ServerPort
    def getClientPort(self):
        return self.ClientPort
    def getSocket(self):
        return self.Socket
    def setClientPort(self,_clientPort):
        self.ClientPort = _clientPort
    def setUserName(self,_username):
        self.Username = _username
    def InitSecurityModule(self,key,PemPath,BackupPemPath):
<<<<<<< HEAD
        self.Security = Security(PemPath,BackupPemPath,key)
=======
        self.Security = Security()
        self.Security.AddClientKey(key)
>>>>>>> 6122c91d5c41b238d5118e4a8e4b9d5b2a0fe91a
    def GetSecurityModule(self):
        return self.Security
    def __repr__(self):
        return  "Username: "+ self.Username+" IP: "+self.Ip+" ServerPort: "+str(self.ServerPort)+" ClientPort: "+str(self.ClientPort)
