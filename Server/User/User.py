class User:
    def __init__(self,_ip):
        self.ip = _ip
        self.online = True
    def getIp(self):
        return self.ip
