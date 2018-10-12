from client import Client
from PIL import ImageTk, Image
from Chat import ChatGUI
from Login import LoginGUI
from SignUp import SignUpGUI

host = '10.102.8.250'
port = 6000
MESSAGE = 'hi'


client = Client(host, port)
client.connectServer()

chat = ChatGUI()
login = LoginGUI()
signUp = SignUpGUI()

login.setSignUpWindow(signUp)
login.setClient(client)
signUp.setLoginWindow(login)
signUp.setClient(client)

# login.withdraw()
signUp.withdraw()


login.mainloop()
