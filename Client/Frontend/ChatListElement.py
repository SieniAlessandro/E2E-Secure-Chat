from tkinter import *
from PIL import ImageTk, Image

class ChatListElement(Frame):
    MAXMESSAGELEN = 15

    def __init__(self, master, background):

        Frame.__init__(self, master)
        self.configure(background=background, padx=10, pady=5)
        self.pack()

        self.photo = ImageTk.PhotoImage(Image.open("crash.jpg").resize( (40,40), Image.ANTIALIAS ))
        self.chatName, self.lastMessage, self.lastMessageTime = StringVar(), StringVar(), StringVar()
        self.createWidgets()

    def changeChatRoom(self, event):
        print("Changing Chat Room...")

    def createWidgets(self):
        photoLabel = Label(self, image = self.photo, )
        chatNameLabel = Label(self, textvariable = self.chatName, background=self['bg'], fg='white', anchor='e')
        lastMessageLabel = Label(self, textvariable = self.lastMessage, background=self['bg'],  fg='white', anchor='e')
        lastMessageTimeLabel = Label(self, textvariable = self.lastMessageTime, background=self['bg'],  fg='white', anchor='e')

        photoLabel.grid(row=0, column=0, rowspan=2, sticky=W, padx=5, pady=5)
        chatNameLabel.grid(row=0,column=1, sticky=W, padx=5)
        lastMessageLabel.grid(row=1,column=1, sticky=W, padx=5)
        lastMessageTimeLabel.grid(row=0,column=2, sticky=W)

        self.bind('<Button-1>', self.changeChatRoom)

    def checkStringLenght(self, s):
        if ( len(s) > self.MAXMESSAGELEN ):
            return s[0:self.MAXMESSAGELEN] + " ..."
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
