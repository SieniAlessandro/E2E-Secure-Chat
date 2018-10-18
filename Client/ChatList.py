from tkinter import *
from PIL import ImageTk, Image
from ChatWindow import ChatWindow as cw
import os

class ChatList(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.chatListDict = {}
        self.grid(row=0, column=0, rowspan=2, sticky=N+S+W)
        self.searchBarFrame = Frame(self, bg=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.searchBar = Entry(self.searchBarFrame, validate = 'focusin', validatecommand = self.resetSearchBarStyle, background=background, bd=0, fg='white')
        self.searchBar.bind('<Return>', self.pressEnterEvent )
        self.icon = ImageTk.PhotoImage(Image.open("Images/searchIcon.png").resize( (30,30), Image.ANTIALIAS ))
        self.searchButton = Button(self.searchBarFrame, text="search", command=self.pressSearchButton, bg=background, bd=0, activebackground='#787878', image=self.icon)
        self.searchBarFrame.grid(column=0, sticky=W+E)
        self.searchBar.pack(side=LEFT, padx=5,pady=5)
        self.searchButton.pack(side=RIGHT, padx=5, pady=5)

    def resetSearchBarStyle(self,event):
        self.searchBarFrame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.searchBarEntry.config(fg='white')

    def pressSearchButton(self):
        username = self.searchBar.get()
        if not username:
            return
        ret = self.client.startConnection(username)
        if ret >= 0:
            self.addChatListElement(username, "", "")
            self.chatListDict[username].changeChatRoom(event='none')
        else:
            self.searchBarFrame.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            self.searchBarEntry.config(fg='red')

    def pressEnterEvent(self, event):
        self.pressSearchButton()

    def setItems(self, chatWindow, client ):
        self.chatWindow = chatWindow
        self.client = client

    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        newChatListElement = ChatListElement(self, self['bg'])
        newChatListElement.setElements(self.chatWindow, chatName, lastMessage, lastMessageTime)
        self.chatListDict[chatName] = newChatListElement

    def notify(self, sender, message, time):
        if sender not in self.c6:
            print("chat not found")
            self.addChatListElement(sender, message, time)
            self.chatListDict[sender].increaseNotifies(message, time)
            if not self.chatWindow.chatName.get():
                self.chatListDict[sender].changeChatRoom(event='none')
                self.chatWindow.addBoxMessageElement(message, time, False)
        else:
            self.chatListDict[sender].increaseNotifies(message, time)

class ChatListElement(Frame):
    MAXMESSAGELEN = 15

    def __init__(self, master, background):

        Frame.__init__(self, master)
        self.configure(background=background, padx=10, pady=5)
        self.grid(column=0, sticky=W+E)
        self.photo = ImageTk.PhotoImage(Image.open("Images/profile.jpg").resize( (40,40), Image.ANTIALIAS ))
        self.chatName, self.lastMessage, self.lastMessageTime = StringVar(), StringVar(), StringVar()
        self.notifies = IntVar()
        self.notifies.set(0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=1)

        self.createWidgets()

    def changeChatRoom(self, event):
        self.chatWindow.changeChatRoom(self.chatName.get())
        self.notifiesLabel.grid_forget()

    def createWidgets(self):
        photoLabel = Label(self, image = self.photo, )
        chatNameLabel = Label(self, textvariable = self.chatName, background=self['bg'], fg='white', anchor=NW)
        lastMessageLabel = Label(self, textvariable = self.lastMessage, background=self['bg'], anchor=NW, fg='white')
        lastMessageTimeLabel = Label(self, textvariable = self.lastMessageTime, background=self['bg'],  anchor=NE, fg='white')
        self.notifiesLabel = Label(self, textvariable = self.notifies, background='#7070db' )

        photoLabel.grid(row=0, column=0, rowspan=2, sticky=W, padx=5, pady=5)
        chatNameLabel.grid(row=0, column=1, sticky=W+E, padx=5)
        lastMessageLabel.grid(row=1,column=1, sticky=W+E, padx=5)
        lastMessageTimeLabel.grid(row=0,column=2, sticky=W+E)

        self.bind('<Button-1>', self.changeChatRoom)
        chatNameLabel.bind('<Button-1>', self.changeChatRoom)
        lastMessageLabel.bind('<Button-1>', self.changeChatRoom)
        photoLabel.bind('<Button-1>', self.changeChatRoom)
        self.notifiesLabel.bind('<Button-1>', self.changeChatRoom)

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

    def increaseNotifies(self, message, time):
        self.listMessage.append(message)
        self.notifies.set(self.notifies.get()+1)
        self.notifiesLabel.grid(row=1, column=2, sticky=W+E)
        self.lastMessage.set(self.checkStringLenght(message))
        self.lastMessageTime.set(time)
