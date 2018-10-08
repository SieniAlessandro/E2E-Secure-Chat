'''
import socket

host = socket.gethostname()
port = 1745
BUFFER_SIZE = 2000
MESSAGE = raw_input("tcpClientA: Enter message/ Enter exit:")

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

while MESSAGE != 'exit':
    tcpClientA.send(MESSAGE)
    data = tcpClientA.recv(BUFFER_SIZE)
    print " Client2 received data:", data
    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")

tcpClientA.close()
'''
import sys

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
root = Tk()
counter = 0;
print(sys.version)
def registration_window(event=None):
    global counter
    counter = counter+1;
    if(counter == 1):
        form = Toplevel(root)
        l = Label(form,text="Ciao")
        l.pack()
def change_color(event=None):
    l1.config(fg="blue")
def orig_color(event=None):
    l1.config(fg="black")

l1 = Label(root,text="Non sei ancora registrato? Clicca qui!!")
l1.bind("<Button-1>",registration_window)
l1.bind("<Enter>",change_color)
l1.bind("<Leave>",orig_color)
l1.grid()
root.mainloop()
