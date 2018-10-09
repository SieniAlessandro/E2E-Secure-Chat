import socket
from threading import Thread
from User.User import User


class ClientHandler(Thread):
    MSG_LEN = 2048
    #Constructor of the class
    #Parameters:
    def __init__(self,Conn,ip,port,db,clients):
        Thread.__init__(self)   #Instatation of the thread
        self.ip = ip
        self.port = port
        self.conn = Conn
        self.DB = db
        self.OnlineClients = clients
        print ("Client gestito all'indirizzo "+ self.ip +" porta "+str(self.port))
    #Method whose listen the message coming from the handled client,showing its content
    def run(self):
        while True:
            data = self.conn.recv(self.MSG_LEN)
            msg = data.decode('utf-16')
            if not data:
                print("Client disconnesso")
                return -1
            print ("Message received: "+msg)
            msgs = msg.split('|')
            if msgs[0] == "1":
                print ("Registrazione")
                param = msgs[1].split(',')
                if (self.DB.insert_user(*param) == 0):
                    self.conn.sendall(("Ti ho registrato "+param[0]).encode('utf-16'))
                else:
                    self.conn.sendall("Errore nella registrazione")
            elif msgs[0] == '2':
                print("Login")
                param = msgs[1].split(',')
                if(self.DB.userIsPresent(*param) == 1):
                    self.conn.sendall("Login OK")
                    self.OnlineClients.append(User(param[0])
                else:
                    self.conn.sendall("Username o password errati")
