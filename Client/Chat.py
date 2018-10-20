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

        self.w = ws*1.5/3 # width for the Tk root
        self.h = hs*2.5/4 # height for the Tk root

        x = (ws/2) - (self.w/2)
        y = (hs/2) - (self.h/2)

        self.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.title("MPS Chat")

        self.protocol("WM_DELETE_WINDOW", self.onCloseEvent )

        # self.iconbitmap(os.getcwd() + '/Images/windowIcon.ico')
        self.resizable(width=FALSE, height=FALSE)
        self.rowconfigure(0,weight=100)
        self.chatWindow = ChatWindow(self, self.backgroundWindow)
        self.chatList = ChatList(self, self.backgroundItems)

    def createWidgets(self, client):
        self.client = client
        self.chatList.setItems(self.chatWindow, self.client)
        self.chatWindow.createWidgets(self.backgroundItems, "", self.client, self.chatList)
        self.chatWindow.scrollableFrame.setCanvasWidth(self.w*3/4)
        self.chatList.scrollableFrame.setCanvasWidth(self.w*1/4)

    def onLoginEvent(self, username):
        self.deiconify()
        self.title("MPS Chat - " + username)
        self.chatList.searchBar.focus_force()
        conversations = self.client.Message.retrieveAllConversations()
        print(conversations)
        for c in conversations.keys():
            for m in conversations[c]:
                self.chatList.notify(c, conversations[c][m]['text'], conversations[c][m]['time'] )

    def onCloseEvent(self):
        print("closing event")
        self.destroy()
        self.client.onClosing()

if __name__ == '__main__':
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    chat = ChatGUI()
    client = Client("", 6555)
    chat.createWidgets(client)

    chat.chatList.addChatListElement("Rododendro", "Oggi piove", None)
    # chat.chatWindow.receiveMessage("Rododendro", "Associated", "0:00")
    chat.mainloop()
