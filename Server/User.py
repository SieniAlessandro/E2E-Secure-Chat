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
    def InitSecurityModule(self,key):
        self.Security = Security()
        self.Security.AddClientKey(key)
    def GetSecurityModule(self):
        return self.Security
    def __repr__(self):
        return  "Username: "+ self.Username+" IP: "+self.Ip+" ServerPort: "+str(self.ServerPort)+" ClientPort: "+str(self.ClientPort)
