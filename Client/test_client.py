from client import Client

host = '10.102.8.250'
port = 6000
MESSAGE = 'hi'

a = Client(host, port)
a.connectServer()
#a.sendServer(MESSAGE)

continua = 1
while(continua) :
    x = int(input('inserire:\ 1-registrarsi\ 2-login\ 3-startConnection\ 0-logout'))
    if x == 1 :
        user = str(input('inserire username : '))
        psw = str(input('inserire psw : '))
        name = str(input('inserire name : '))
        surname = str(input('inserire surname : '))
        email = str(input('inserire email : '))
        a.register(user,psw,name,surname,email,'0')
    elif x == 2 :
        user = str(input('inserire username : '))
        psw = str(input('inserire psw : '))
        a.login(user,psw)
    elif x == 3 :
        receiver = str(input('inserire username del ricevitore'))
        a.startConnection(receiver)
    elif x == 0 :
        continua = not continua
#while MESSAGE != 'exit':

#a.register('nuovoUser','pwd','pippo','gianfilippo','pippo@mail.com','0')

a.login('nuovoUser','pwd')
#data = tcpClientA.recv(BUFFER_SIZE)
#print " Client2 received data:", data
#MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")

#a.socketServer.close()
