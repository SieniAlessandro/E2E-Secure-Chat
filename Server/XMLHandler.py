#import xml.etree.ElementTree as ET
from lxml import etree
class XMLHandler:
    PATH = "preferences.xml"
    def __init__(self):
        try:
            self.root = etree.fromstring(open(self.PATH,"r").read())
        except FileNotFoundError:
            print("Creo un nuovo file")
            self.initilizeXML()
            self.root = etree.fromstring(open(self.PATH,"r").read())


    def initilizeXML(self):
        root = etree.Element('Server')

        #General Config
        server_port = etree.SubElement(root,"ListenPort")
        server_port.text = "6000"
        EnableLog = etree.SubElement(root,"EnableLog")
        EnableLog.text = "1"

        # Database
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

        #Writing in the file
        tree = etree.ElementTree(root)
        tree.write(self.PATH,pretty_print=True)

    def getDatabasePort(self):
        return int(self.root[2][1].text)
    def getDatabaseAddress(self):
        return self.root[2][0].text
    def getDatabaseUser(self):
        return self.root[2][2].text
    def getDatabasePwd(self):
        return self.root[2][3].text
    def getServerPort(self):
        return int(self.root[0].text)
    def getDatabaseName(self):
        return self.root[2][4].text
