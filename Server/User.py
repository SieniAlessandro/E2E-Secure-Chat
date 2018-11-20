from Security.Security import Security

class User:
    def __init__(self,_socket,_ip,_ClientPort,_ServerPort,_UserName):
        """ Instatiate all the information about the user
            Parameter:
                    _socket     : The socket used by the server to communicate with this user   : Socket
                    _ip         : The IP address of this user                                   : string
                    _ClientPort : The port used by the user to listen from other clients        : int
                    _ServerPort : The port used by the user to listen from the server           : int
                    _UserName   : The username of this user (Probably in this moment is None)   : string
            Return:
                    Void - Constructor"""
        self.Ip = _ip
        self.ClientPort = _ClientPort
        self.ServerPort = _ServerPort
        self.Username = _UserName
        self.Socket = _socket

    def getUserName(self):
        """ Get the username of this user
            Parameter :
                    Void
            Return:
                    The username of this user"""
        return self.Username

    def getIp(self):
        """ Get the IP address of this user
            Parameter:
                    Void
            Return:
                    The IP address of this user     : string"""
        return self.Ip

    def getServerPort(self):
        """ Get the port used by the user to listen from the server
            Parameter:
                    Void
            Return:
                    The port used by the user to listen from the server     : int """
        return self.ServerPort

    def getClientPort(self):
        """ Get the port used by the user to listen from other clients
            Parameter:
                    Void
            Return:
                    The port used by the user to listen from the other clients     : int """
        return self.ClientPort

    def getSocket(self):
        """ Get the socket used to communicate with this user
            Parameter:
                    Void
            Return:
                    The port used to communicate with this user     : Socket """
        return self.Socket

    def setClientPort(self,_clientPort):
        """ Set the port used by the user to listen from other clients
            Parameter:
                    _clientPort: The port used by the user to listen from other clients     : int
            Return:
                    Void    """
        self.ClientPort = _clientPort

    def setUserName(self,_username):
        """ Set the username of this user
            Parameter:
                    _username: the username to associate    : string
            Return:
                    Void """
        self.Username = _username

    def addSecurityModule(self,Security):
        """ Add the security module for this user
            Parameter:
                    Security: The security object   : Security
            Return:
                    Void """
        self.Security = Security

    def GetSecurityModule(self):
        """ Get the security module in order to use its own method
            Parameter:
                    Void
            Return:
                    The security Module     : Security"""
        return self.Security

    def __repr__(self):
        """ Represent the object as a string, usefull whenyou have to print an array of object
            Parameter :
                    Void
            Return:
                    The string meaning the parameter of the user        : string"""
        return  "Username: "+ self.Username+" IP: "+self.Ip+" ServerPort: "+str(self.ServerPort)+" ClientPort: "+str(self.ClientPort)
