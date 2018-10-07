from tkinter import *
from PIL import ImageTk, Image

class ChatListElement(Frame):
    MAXMESSAGELEN = 15

    def __init__(self, master):

        Frame.__init__(self,master)
        self.pack()

        self.photo = ImageTk.PhotoImage(Image.open("crash.jpg").resize( (40,40), Image.ANTIALIAS ))
        self.chatName, self.lastMessage, self.lastMessageTime = StringVar(), StringVar(), StringVar()
        self.setElements("ChatName", "lastMessage", "0:00")
        self.createWidgets()

    def changeChatRoom(self, event):
        print("Changing Chat Room")

    def createWidgets(self):
        subFrame = Frame(self)
        photoLabel = Label(self, image = self.photo)
        self.chatNameLabel = Label(subFrame, textvariable = self.chatName)
        self.lastMessageLabel = Label(subFrame, textvariable = self.lastMessage)
        self.lastMessageTimeLabel = Label(subFrame, textvariable = self.lastMessageTime )

        photoLabel.grid(row=0,column=0)
        subFrame.grid(row=0,column=1)
        self.chatNameLabel.grid(row=0,column=0)
        self.lastMessageLabel.grid(row=1,column=0)
        self.lastMessageTimeLabel.grid(row=0,column=1)

        # self.bind('<Button-1>', self.changeChatRoom)

    def checkStringLenght(self, s):
        if ( len(s) > self.MAXMESSAGELEN ):
            return s[0:15] + " ..."
        return s

    def setLastMessage(self, message):
        self.lastMessage.set(self.checkStringLenght(message))

    def setChatName(self, chatName):
        self.chatName.set(self.checkStringLenght(chatName))

    def setLastMessageTime(self, lastMessageTime):
        self.lastMessageTime.set(lastMessageTime)

    def setElements(self, chatName, lastMessage, lastMessageTime):
        self.chatName.set(self.checkStringLenght(chatName))
        self.lastMessage.set(self.checkStringLenght(lastMessage))
        self.lastMessageTime.set(lastMessageTime)
        self.createWidgets()
