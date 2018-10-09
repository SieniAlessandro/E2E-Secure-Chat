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
                if self.ip in self.OnlineClients.values():
                    self.OnlineClients.remove(self.ip)
                return -1
            print ("Message received: "+msg)
            msgs = msg.split('|')
            if msgs[0] == "1":
                print ("Registrazione")
                param = msgs[1].split(',')
                if (self.DB.insert_user(*param) == 0):
                    self.conn.sendall(("Ti ho registrato "+param[0]).encode('utf-16'))
                else:
                    self.conn.sendall("Errore nella registrazione".encode('utf-16'))
            elif msgs[0] == '2':
                print("Login")
                print("Ip del client: " + self.ip)
                param = msgs[1].split(',')
                response = ""
                #Check if this user is already Logged In
                if self.ip in self.OnlineClients.values:
                    response = "?|"+str(-1)
                elif self.DB.userIsPresent(*param) == 1:
                    response = "?|"+str(1)
                    self.OnlineClients[param[0]] = self.ip
                else:
                    response = "?|"+str(0)
                self.conn.send(response.encode('utf-16'))
                print(self.OnlineClients)
            elif msgs[0] == '3':
                print("Richiesta di utente online")
                response = ""
                #Check if the clients is logged in
                if self.ip not in self.OnlineClients.values():
                    response = "!|"+str(-1)
                else:
                    if msgs[1] in self.OnlineClients.keys():
                        #Check if the client asks for its own import ip
                        if self.OnlineClients[msgs[1]] == self.ip:
                            response = "!|"+str(-2)
                        #Otherwise the server provide the ip of the client
                        else:
                            response = "!|"+self.OnlineClients[msgs[1]]
                    else:
                        response = "!|"+str(0)
                self.conn.send(response.encode('utf-16'))
