from lxml import etree
import lxml.builder

class XMLClientHandler:

    PATH = "settings.xml"
    def __init__(self):
        try:
            self.root = etree.fromstring(open(self.PATH,"r").read())
        except FileNotFoundError:
            print("Creo un nuovo file")
            self.initilizeXML()


    def initilizeXML(self):
        root = etree.Element('Client')

        # General Config
        EnableLog = etree.SubElement(root,"EnableLog")
        EnableLog.text = "1"

        # Server
        server = etree.SubElement(root,"Server")
        server_port = etree.SubElement(server,"ServerPort")
        server_port.text = "6000"
        server_address = etree.SubElement(server,"ServerAddress")
        server_address.text = "127.0.0.1"

        # User
        auto = etree.SubElement(root,"AutoLogin")
        user_remember = etree.SubElement(auto, "remember")
        user_remember.text = "0"
        user_name = etree.SubElement(auto,"UserName")
        user_name.text = '-'
        user_pwd = etree.SubElement(auto,"Password")
        user_pwd.text = "-"

        #Writing in the file
        tree = etree.ElementTree(root)
        tree.write(self.PATH,pretty_print=True)

    def getServerPort(self):
        return int(self.root[1][0].text))
    def getServerAddress(self):
        return self.root[1][1].text
    def getRemember(self):
        return self.root[2][0].text
    def getUserName(self):
        return self.root[2][1].text
    def getUserPwd(self):
        return self.root[2][2].text
    def getEnableLog(self):
        return self.root[0][0].text

    def setAutoLogin(self, remember, user, psw):
        self.root[2][0].text = str(remember)
        self.root[2][1].text = user
        self.root[2][2].text = pwd

    def saveXML(self):
        tree = etree.ElementTree(self.root)
        tree.write(self.PATH,pretty_print=True)
