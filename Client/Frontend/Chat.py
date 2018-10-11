from tkinter import *
from ChatList import ChatList
from ChatWindow import *

class ChatGUI(Tk):
    backgroundWindow = '#47476b'
    backgroundItems = '#29293d'
    def __init__(self):
        Tk.__init__(self)
        self.title("Chat")
        self.geometry('1024x720')
        self.resizable(width=FALSE, height=FALSE)
        self.columnconfigure(1, weight=6)
        self.rowconfigure(0,weight=4)

        self.chatWindow = ChatWindow(self, self.backgroundWindow)
        self.chatWindow.createWidgets(self.backgroundItems, "Federico")

        self.chatList = ChatList(self, self.backgroundItems)
        self.chatList.setChatWindow(self.chatWindow)

        self.inputBar = InputBar(self, self.backgroundItems)
        self.inputBar.setChatWindow(self.chatWindow)

    def fillChatList(self, chatList):
        for i in chatList:
            self.chatList.addChatListElement(i.chatName, i.lastMessage, i.lastMessageTime)


chat = ChatGUI()

chat.chatList.addChatListElement("Rododendro", "Oggi piove", "18:12")
chat.mainloop()
