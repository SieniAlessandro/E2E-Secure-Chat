from client import Client
from PIL import ImageTk, Image
from Chat import ChatGUI
from Login import LoginGUI
from SignUp import SignUpGUI
import os
import ctypes
import sys

host = '127.0.0.1'#'10.102.11.147'
port = 6000
MESSAGE = 'hi'

if os.getcwd().find("Client") == -1:
    os.chdir("Client")

if sys.platform.startswith('win'):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

chat = ChatGUI()
login = LoginGUI()
signUp = SignUpGUI()
client = Client(chat.chatList)


chat.withdraw()
login.withdraw()
signUp.withdraw()

chat.createWidgets(client, login)
client.connectServer()

login.setSignUpWindow(signUp)
login.setItems(client, chat)
signUp.setLoginWindow(login)
signUp.setClient(client)

ret = client.checkAutoLogin()
if ret == 1:
    chat.onLoginEvent(client.username)
else:
    if ret == 0 :
        login.showError()
    elif ret == -1:
        login.showMessage("You are already logged in other device",  "#ff1a1a" )
    login.deiconify()

login.mainloop()
