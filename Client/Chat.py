from tkinter import *
from ChatList import ChatList
from ChatWindow import *
from client import Client
import os

class ChatGUI(Tk):
    backgroundWindow = '#47476b'
    backgroundItems = '#29293d'
    def __init__(self):
        Tk.__init__(self)

        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        w = ws*1.5/3 # width for the Tk root
        h = hs*2.5/4 # height for the Tk root

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("MPS Chat")
        self.resizable(width=FALSE, height=FALSE)
        self.columnconfigure(1, weight=6)
        self.rowconfigure(0,weight=4)

    def fillChatList(self, chatList):
        for i in chatList:
            self.chatList.addChatListElement(i.chatName, i.lastMessage, i.lastMessageTime)

    def createWidgets(self, client):
        self.client = client
        self.chatWindow = ChatWindow(self, self.backgroundWindow)
        self.chatWindow.createWidgets(self.backgroundItems, "", self.client)

        self.chatList = ChatList(self, self.backgroundItems)
        self.chatList.setItems(self.chatWindow, self.client)

    def onLoginEvent(self):
        self.deiconify()
        self.chatList.searchBar.focus_force()

        # carica chatList
        # apri la prima chat nell'elenco
        # carica i messaggi della chat aperta

if __name__ == '__main__':
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    chat = ChatGUI()
    client = Client("", 6555)
    chat.createWidgets(client)

    chat.chatList.addChatListElement("Rododendro", "Oggi piove", "18:12")
    chat.iconbitmap(os.getcwd() + '/Images/windowIcon.ico')
    chat.mainloop()
