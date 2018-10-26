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
        user = etree.SubElement(root,"User")
        user_remember = etree.SubElement(user, "Remember")
        user_remember.text = "0"
        user_name = etree.SubElement(user,"UserName")
        user_name.text = '-'
        user_pwd = etree.SubElement(user,"Password")
        user_pwd.text = "-"

        #Writing in the file
        tree = etree.ElementTree(root)
        tree.write(self.PATH,pretty_print=True)
'''
    def getDatabasePort(self):
        return int(self.root[2][1].text))
    def getDatabaseAddress(self):
        return self.root[2][0].text
    def getDatabaseUser(self):
        return self.root[2][2]
    def.getDatabasePwd(self):
        return self.root[2][3]
    def.getServerPort(self):
        return int(self.root[0])
'''
