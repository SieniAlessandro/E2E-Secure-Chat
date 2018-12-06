from lxml import etree
import lxml.builder
import os

class XMLClientHandler:
    """Module used to read the configuration of the client from an XML file """

    PATH = "Local/settings.xml"
    def __init__(self):
        """
            Open the XML file from the default PATH (Local/preferences.xml) and if it is not present, create it and write
            default configuration
        """
        try:
            self.root = etree.fromstring(open(self.PATH,"r").read())
        except FileNotFoundError:
            try:
                os.stat("Local")
            except:
                os.mkdir("Local")
            #print("Creo un nuovo file")
            self.initilizeXML()


    def initilizeXML(self):
        """
            Intialize a new XML file with the default configuration
        """
        self.root = etree.Element('Client')

        # General Config
        EnableLog = etree.SubElement(self.root,"EnableLog")
        EnableLog.text = "1"

        # Server
        server = etree.SubElement(self.root,"Server")
        server_port = etree.SubElement(server,"ServerPort")
        server_port.text = "6000"
        server_address = etree.SubElement(server,"ServerAddress")
        server_address.text = "127.0.0.1"

        # User
        auto = etree.SubElement(self.root,"AutoLogin")
        user_remember = etree.SubElement(auto, "remember")
        user_remember.text = "0"
        user_name = etree.SubElement(auto,"UserName")
        user_name.text = '-'
        user_pwd = etree.SubElement(auto,"Password")
        user_pwd.text = "-"

        # Security
        sec = etree.SubElement(self.root, "Security")
        sec_path = etree.SubElement(sec, "path")
        sec_path.text = "SecurityClient/PrivateKey"
        sec_path = etree.SubElement(sec, "serverPubKeyPath")
        sec_path.text = "SecurityClient/ServerPublicKey.pem"
        sec_path = etree.SubElement(sec, "parametersDH")
        sec_path.text = "SecurityClient/ParametersDH"
        #Writing in the file
        tree = etree.ElementTree(self.root)
        tree.write(self.PATH,pretty_print=True)

    def getEnableLog(self):
        """
            Obtain the boolean variable meaning if the Log must be enable or not

            :rtype: Boolean
            :return: The boolean variable meaning if the Log must be enable or not
        """
        return int(self.root[0].text)
    def getServerPort(self):
        """
            Obtain the port used by the server to listen for new requests

            :rtype: Int
            :return: The port used by the server to listen for new requests
        """
        return int(self.root[1][0].text)
    def getServerAddress(self):
        """
            Obtain the IP address of the server

            :rtype: String
            :return: The IP address of the server
        """
        return self.root[1][1].text
    def getRemember(self):
        """
            Obtain the boolean variable meaning if the AutoLogin is enabled or not

            :rtype: Boolean
            :return: The boolean variable meaning if the AutoLogin is enabled or not
        """
        return int(self.root[2][0].text)
    def getUserName(self):
        """
            Obtain the name of the username to do the AutoLogin

            :rtype: String
            :return: The name of the username to do the AutoLogin
        """
        return self.root[2][1].text
    def getUserPwd(self):
        """
            Obtain the name of the password to do the AutoLogin

            :rtype: String
            :return: The name of the password to do the AutoLogin
        """
        return self.root[2][2].text
    def getSecurityPath(self):
        """
            Obtain the path of the security folder

            :rtype: String
            :return: The path of the security folder
        """
        return self.root[3][0].text
    def getSecurityServerKey(self):
        """
            Obtain the path of the server public key

            :rtype: String
            :return: The path of the server public key
        """
        return self.root[3][1].text
    def getSecurityParameters(self):
        """
            Obtain the path of the diffie hellman public parameters

            :rtype: String
            :return: The path of the diffie hellman public parameters
        """
        return self.root[3][2].text

    def setAutoLogin(self, remember, user, password):
        """
            Modify the values relative to the AutoLogin parameters
        """
        self.root[2][0].text = str(remember)
        self.root[2][1].text = user
        self.root[2][2].text = password

    def saveXML(self):
        """
            Save the XML file
        """
        tree = etree.ElementTree(self.root)
        tree.write(self.PATH,pretty_print=True)
