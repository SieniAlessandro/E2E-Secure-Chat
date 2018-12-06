from Security.Security import Security

class User:
    def __init__(self,_socket,_ip,_ClientPort,_ServerPort,_UserName):
        """
            Instatiate all the information about the user

            :type _socket: Socket
            :param _socket: The socket used by the server to communicate with this user
            :type _ip: string
            :param _ip: The IP address of this user
            :type _ClientPort: int
            :param _ClientPort: The port used by the user to listen from other clients
            :type _ServerPort: int
            :param _ServerPort: The port used by the user to listen from the server
            :type _UserName: string
            :param _UserName: The username of this user (Probably in this moment is None)
        """
        self.Ip = _ip
        self.ClientPort = _ClientPort
        self.ServerPort = _ServerPort
        self.Username = _UserName
        self.Socket = _socket

    def getUserName(self):
        """
            Get the username of this user

            :rtype: String
            :return: The username of this user
        """
        return self.Username

    def getIp(self):
        """
            Get the IP address of this user

            :rtype: String
            :return: The IP address of this user
            """
        return self.Ip

    def getServerPort(self):
        """
            Get the port used by the user to listen from the server

            :rtype: int
            :return: The port used by the user to listen from the server
        """
        return self.ServerPort

    def getClientPort(self):
        """
            Get the port used by the user to listen from other clients

            :rtype: int
            :return: The port used by the user to listen from the other clients
        """
        return self.ClientPort

    def getSocket(self):
        """
            Get the socket used to communicate with this user

            :rtype: Socket
            :return: The port used to communicate with this user
        """
        return self.Socket

    def setClientPort(self,_clientPort):
        """
            Set the port used by the user to listen from other clients

            :type _clientPort: int
            :param _clientPort: The port used by the user to listen from other clients
         """
        self.ClientPort = _clientPort

    def setUserName(self,_username):
        """
            Set the username of this user

            :type _username: String
            :param _username: the username to associate
        """
        self.Username = _username

    def addSecurityModule(self,Security):
        """
            Add the security module for this user

            :type Security: Security
            :param Security: The security object
        """
        self.Security = Security

    def GetSecurityModule(self):
        """
            Get the security module in order to use its own method

            :rtype: Security
            :return: The security Module
        """
        return self.Security

    def __repr__(self):
        """
            Represent the object as a string, usefull when you have to print an array of User

            :rtype: String
            :return: The string meaning the parameter of the user
        """
        return  "Username: "+ self.Username+" IP: "+self.Ip+" ServerPort: "+str(self.ServerPort)+" ClientPort: "+str(self.ClientPort)
