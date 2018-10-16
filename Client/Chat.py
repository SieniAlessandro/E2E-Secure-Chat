from tkinter import *
from ChatList import ChatList
from ChatWindow import *

class ChatGUI(Tk):
    backgroundWindow = '#47476b'
    backgroundItems = '#29293d'
    def __init__(self):
        Tk.__init__(self)
        w = 1024 # width for the Tk root
        h = 720 # height for the Tk root

        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("Chat")
        self.geometry('1024x720')
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

        self.inputBar = InputBar(self, self.backgroundItems)
        self.inputBar.setItems(self.chatWindow, self.client)

chat = ChatGUI()

chat.chatList.addChatListElement("Rododendro", "Oggi piove", "18:12")
chat.mainloop()
