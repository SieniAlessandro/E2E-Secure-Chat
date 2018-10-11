from tkinter import *
from PIL import ImageTk, Image
from Chat import chatWindow as cw

class ChatList(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.list = []
        self.grid(row=0, column=0, rowspan=2, sticky=N+S+W)

    def setChatWindow(self, chatWindow ):
        self.chatWindow = chatWindow

    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        newChatListElement = ChatListElement(self, self['bg']).setElements(self.chatWindow, chatName, lastMessage, lastMessageTime)
        self.list.append(newChatListElement)

class ChatListElement(Frame):
    MAXMESSAGELEN = 15

    def __init__(self, master, background):

        Frame.__init__(self, master)
        self.configure(background=background, padx=10, pady=5)
        self.grid(column=0, sticky=W+E)
        self.photo = ImageTk.PhotoImage(Image.open("Client/Frontend/images.png").resize( (40,40), Image.ANTIALIAS ))
        self.chatName, self.lastMessage, self.lastMessageTime = StringVar(), StringVar(), StringVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=1)

        self.createWidgets()

    def changeChatRoom(self, event):
        print("Changing Chat Room...")
        self.chatWindow.changeChatRoom(self.chatName.get())

    def createWidgets(self):
        photoLabel = Label(self, image = self.photo, )
        chatNameLabel = Label(self, textvariable = self.chatName, background=self['bg'], fg='white', anchor=NW)
        lastMessageLabel = Label(self, textvariable = self.lastMessage, background=self['bg'], anchor=NW, fg='white')
        lastMessageTimeLabel = Label(self, textvariable = self.lastMessageTime, background=self['bg'],  anchor=NE, fg='white')

        photoLabel.grid(row=0, column=0, rowspan=2, sticky=W, padx=5, pady=5)
        chatNameLabel.grid(row=0, column=1, sticky=W+E, padx=5)
        lastMessageLabel.grid(row=1,column=1, sticky=W+E, padx=5)
        lastMessageTimeLabel.grid(row=0,column=2, sticky=W+E)

        self.bind('<Button-1>', self.changeChatRoom)
        chatNameLabel.bind('<Button-1>', self.changeChatRoom)
        lastMessageLabel.bind('<Button-1>', self.changeChatRoom)
        lastMessageLabel.bind('<Button-1>', self.changeChatRoom)
        photoLabel.bind('<Button-1>', self.changeChatRoom)

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

    def setElements(self, chatWindow, chatName, lastMessage, lastMessageTime):
        self.chatWindow = chatWindow
        self.chatName.set(self.checkStringLenght(chatName))
        self.lastMessage.set(self.checkStringLenght(lastMessage))
        self.lastMessageTime.set(lastMessageTime)
