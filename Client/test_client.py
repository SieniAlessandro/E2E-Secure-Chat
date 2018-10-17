from client import Client
import os

host = '10.102.23.156'#'127.0.0.1'
port = 6000
MESSAGE = 'hi'

a = Client(host, port)
a.connectServer()
#a.sendServer(MESSAGE)

continua = 1
while(continua) :
    try:
        x = int(input('inserire:\n 1-registrarsi\n 2-login\n 3-startConnection\n 4-sendMessage\n 0-logout\n'))
    except:
        print('Wrong values had been inserted, try again')
        continue
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
        receiver = str(input('inserire username dell\'utente con cui ti vuoi connettere'))
        a.startConnection(receiver)
    elif x == 4 :
        receiver = str(input('inserire username del ricevitore : '))
        text = str(input('inserire il testo da inviare : '))
        a.sendClient(receiver, text)
    elif x == 0 :
        print('Exiting...')
        os._exit(0)
#while MESSAGE != 'exit':

#a.register('nuovoUser','pwd','pippo','gianfilippo','pippo@mail.com','0')

#a.login('nuovoUser','pwd')
#data = tcpClientA.recv(BUFFER_SIZE)
#print " Client2 received data:", data
#MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")

#a.socketServer.close()
