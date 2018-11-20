from lxml import etree


class XMLHandler:
    """Module used to read the configuration of the server from an XML file """

    PATH = "preferences.xml"
    def __init__(self):
        """ Open the XML file from the default PATH (preferences.xml) and if it is not present, create it and write
            default configuration
            Parameter:
                    Void
            Return:
                    Void - Constructor"""
        try:
            self.root = etree.fromstring(open(self.PATH,"r").read())
        except FileNotFoundError:
            self.initilizeXML()

    def initilizeXML(self):
        """ Intialize a new XML file with the default configuration:
            Parameter:
                    Void
            Return:
                    Void        """

        root = etree.Element('Server')

        #General Config
        server_port = etree.SubElement(root,"ListenPort")
        server_port.text = "6000"
        EnableLog = etree.SubElement(root,"EnableLog")
        EnableLog.text = "1"
        LogPath = etree.SubElement(root,"LogPath")
        LogPath.text = "tempLog.txt"

        #Database
        db = etree.SubElement(root,"Database")
        db_addr = etree.SubElement(db,"Address")
        db_addr.text = "127.0.0.1"
        db_port = etree.SubElement(db,"Port")
        db_port.text = "3306"
        db_user = etree.SubElement(db,"User")
        db_user.text = "root"
        db_pwd = etree.SubElement(db,"Password")
        db_pwd.text = "rootroot"
        db_name = etree.SubElement(db,"name")
        db_name.text = "messaggistica_mps"

        #Security
        PemPath = etree.SubElement(root,"PemPath")
        PemPath.text = "Security/PrivateKey.pem"
        BackupPemPath = etree.SubElement(root,"PemPath")
        BackupPemPath.text = "Security/Backup/PrivateKey.pem"

        #Writing in the file
        tree = etree.ElementTree(root)
        tree.write(self.PATH,pretty_print=True)

        self.root = root

    def getDatabasePort(self):
        """ Obtain the port used by the DBMS to listen new requests
            Parameter:
                    Void
            Return:
                    The port used by the DBMS to listen new requests    : int   """
        return int(self.root[3][1].text)

    def getDatabaseAddress(self):
        """ Obtain the IP address of the database
            Parameter:
                    Void
            Return:
                    The IP address of the database           : string   """
        return self.root[3][0].text

    def getDatabaseUser(self):
        """ Obtain the username to login on the database
            Parameter:
                    Void
            Return:
                    The username to login on the database           : string   """
        return self.root[3][2].text

    def getDatabasePwd(self):
        """ Obtain the password to login on the database
            Parameter:
                    Void
            Return:
                    The password to login on the database           : string   """
        return self.root[3][3].text

    def getServerPort(self):
        """ Obtain the port used by the server to listen for new requests
            Parameter:
                    Void
            Return:
                    The port used by the server to listen for new requests           : int   """
        return int(self.root[0].text)

    def getDatabaseName(self):
        """ Obtain the name of the database
            Parameter:
                    Void
            Return:
                    The name of the database           : string   """
        return self.root[3][4].text

    def getEnableLog(self):
        """ Obtain the boolean variable meaning if the Log must be enable or not
            Parameter:
                    Void
            Return:
                    The boolean variable meaning if the Log must be enable or not           : Boolean   """
        return int(self.root[1].text)

    def GetLogPath(self):
        """ Obtain the path of the log file
            Parameter:
                    Void
            Return:
                    The path of the log file          : string   """
        return self.root[2].text

    def getPemPath(self):
        """ Obtain the path of the pem file with the private key of the server
            Parameter:
                    Void
            Return:
                    The path of the pem file with the private key of the server          : string   """
        return self.root[4].text

    def getBackupPemPath(self):
        """ Obtain the path of the backup pem file with the private key of the server
            Parameter:
                    Void
            Return:
                    The path of the backup pem file with the private key of the server          : string   """
        return self.root[5].text
