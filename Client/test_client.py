import socket

host = '127.0.0.1'
port = 6000
BUFFER_SIZE = 2000
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))
MESSAGE = input("tcpClientA: Enter message/ Enter exit:")
print (str(MESSAGE))
tcpClientA.send(MESSAGE.encode('utf-16'))
print (tcpClientA.recv(2000).decode('utf-16'))

'''
while MESSAGE != 'exit':
    tcpClientA.send(MESSAGE)
    data = tcpClientA.recv(BUFFER_SIZE)
    print " Client2 received data:", data
    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")

tcpClientA.close()
'''
