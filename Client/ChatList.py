from tkinter import *
from PIL import ImageTk, Image
from ChatWindow import ChatWindow as cw
from ScrollableFrame import *
import os


class ChatList(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.chatListDict = {}

        self.grid(row=0, column=0, sticky=N+S+W+E)
        self.searchBarFrame = Frame(self, bg=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        listFrame = Frame(self)
        self.scrollableFrame = Scrollable(listFrame, background)
        self.searchBar = Entry(self.searchBarFrame, background=background, bd=0, fg='white')
        self.searchBar.bind('<Return>', self.pressEnterEvent )
        self.icon = ImageTk.PhotoImage(Image.open("Images/searchIcon.png").resize( (30,30), Image.ANTIALIAS ))
        self.searchButton = Button(self.searchBarFrame, text="search", command=self.pressSearchButton, bg=background, bd=0, activebackground='#787878', image=self.icon)

        self.searchBarFrame.pack(side="top", fill=X)
        self.searchBar.pack(side=LEFT, padx=5,pady=5)
        self.searchButton.pack(side=RIGHT, padx=5, pady=5)
        listFrame.pack(fill=BOTH, expand=True)

    def pressSearchButton(self):
        username = self.searchBar.get()
        searchKey = username.lower()
        if not username:
            return
        if searchKey not in self.chatListDict:
            ret = self.client.startConnection(username)
            if ret >= 0:
                self.addChatListElement(username, "", lastMessageTime=None)
                self.chatListDict[searchKey].changeChatRoom(event='none')
                self.searchBarFrame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
                self.searchBar.config(fg='white')
                self.searchBar.delete(0, 'end')
            else:
                self.searchBarFrame.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.searchBar.config(fg='red')
        else:
            self.chatListDict[searchKey].changeChatRoom(event='none')

    def pressEnterEvent(self, event):
        self.pressSearchButton()

    def setItems(self, chatWindow, client ):
        self.chatWindow = chatWindow
        self.client = client

    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        if lastMessageTime is None:
            timeString = '-:--'
        else:
            timeString = str(lastMessageTime).split('.')[0].split(' ')[1][:-3]
        newChatListElement = ChatListElement(self.scrollableFrame, self['bg'])
        newChatListElement.setElements(self.chatWindow, chatName, lastMessage, timeString)
        self.chatListDict[chatName.lower()] = newChatListElement
        self.scrollableFrame.update()
        self.scrollableFrame.canvas.yview_moveto( 1 )

    def notify(self, sender, message, time, isMine):
        searchKey = sender.lower()
        if searchKey not in self.chatListDict:
            #chatList not found in the list
            print("Adding chat with " + sender)
            self.addChatListElement(sender, message, time)
            self.client.startConnection(sender)
        if not self.chatWindow.chatName.get():
            # chatWindow has no active chat
            self.chatListDict[searchKey].changeChatRoom(event=None)
            self.chatWindow.addBoxMessageElement(message, time, isMine)
        elif self.chatWindow.chatName.get() == sender:
            #sender chat is active
            self.chatWindow.addBoxMessageElement(message, time, isMine)
        else:
            #there is an active chat but not the sender's one, so notify that
            self.chatListDict[searchKey].increaseNotifies(message, time)

    def updateMessageTime(self, chatName, message, time):
        searchKey = chatName.lower()
        self.chatListDict[searchKey].setLastMessage(message)
        self.chatListDict[searchKey].setLastMessageTime(time)

class ChatListElement(Frame):
    MAXMESSAGELEN = 15

    def __init__(self, master, background):

        Frame.__init__(self, master)
        self.configure(background=background, padx=10, pady=5)
        self.pack(fill=X)
        self.photo = ImageTk.PhotoImage(Image.open("Images/profile.jpg").resize( (40,40), Image.ANTIALIAS ))
        self.chatName, self.lastMessage, self.lastMessageTime = StringVar(), StringVar(), StringVar()
        self.notifies = IntVar()
        self.notifies.set(0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=1)

        self.createWidgets()

    def changeChatRoom(self, event):
        if self.chatName.get() == self.chatWindow.chatName.get():
            return
        fill = False if event is None else True
        self.chatWindow.changeChatRoom(self.chatName.get(), fill)
        self.notifies.set(0)
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
        timeString = str(lastMessageTime).split('.')[0].split(' ')[1][:-3]
        self.lastMessageTime.set(timeString)

    def setElements(self, chatWindow, chatName, lastMessage, lastMessageTime):
        self.chatWindow = chatWindow
        self.chatName.set(self.checkStringLenght(chatName))
        self.lastMessage.set(self.checkStringLenght(lastMessage))
        self.lastMessageTime.set(lastMessageTime)

    def increaseNotifies(self, message, time):
        self.notifies.set(self.notifies.get()+1)
        self.notifiesLabel.grid(row=1, column=2, sticky=W+E)
        self.setLastMessage(message)
        self.setLastMessageTime(time)
