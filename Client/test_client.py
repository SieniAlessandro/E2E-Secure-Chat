from client import Client

host = '10.102.7.116'
port = 6000
MESSAGE = 'hi'

a = Client(host, port)
a.connectServer()

#while MESSAGE != 'exit':
a.sendServer(MESSAGE)

a.register()
#data = tcpClientA.recv(BUFFER_SIZE)
#print " Client2 received data:", data
#MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")

#a.socketServer.close()
