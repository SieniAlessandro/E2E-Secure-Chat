from client import Client
from PIL import ImageTk, Image
from Chat import ChatGUI
from Login import LoginGUI
from SignUp import SignUpGUI

host = ''
port = 6000
MESSAGE = 'hi'


client = Client("", port)
client.connectServer()

chat = ChatGUI()
login = LoginGUI()
signUp = SignUpGUI()

login.setSignUpWindow(signUp)
login.setClient(client)
signUp.setLoginWindow(login)
signUp.setClient(client)
chat.setClient(client)

# chat.withdraw()
signUp.withdraw()


login.mainloop()
