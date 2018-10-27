from tkinter import *
from PIL import ImageTk, Image
from ChatWindow import *
from ScrollableFrame import *
import os

activeChat = None

class ChatList(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.chatListDict = {}
        self.master = master

        self.pack(side=LEFT,fill=BOTH)
        self.searchBarFrame = Frame(self, bg=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        listFrame = Frame(self)
        self.scrollableFrame = Scrollable(listFrame, background)
        self.searchBar = Entry(self.searchBarFrame, background=background, bd=0, fg='white')
        self.searchBar.bind('<Return>', self.pressEnterEvent )
        self.searchIcon = ImageTk.PhotoImage(Image.open("Images/searchIcon.png").resize( (30,30), Image.ANTIALIAS ))
        self.searchButton = Button(self.searchBarFrame, text="search", command=self.pressSearchButton, bg=background, bd=0, activebackground='#787878', image=self.searchIcon)

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
            ret = self.client.startConnection(searchKey)
            if ret >= 0:
                self.addChatListElement(username, "", lastMessageTime=None)
                activeChat = self.chatListDict[searchKey][1]
                self.chatListDict[searchKey][0].changeChatRoom(event=None)
                self.searchBarFrame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
                self.searchBar.config(fg='white')
                self.searchBar.delete(0, 'end')
            else:
                self.searchBarFrame.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.searchBar.config(fg='red')
        else:
            self.chatListDict[searchKey][0].changeChatRoom(event='none')

    def pressEnterEvent(self, event):
        self.pressSearchButton()

    def setItems(self, client ):
        self.client = client

    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        if lastMessageTime is None:
            timeString = '-:--'
        else:
            timeString = str(lastMessageTime).split('.')[0].split(' ')[1][:-3]

        newChatListElement = ChatListElement(self.scrollableFrame, self['bg'])
        newChatWindow = ChatWindow(self.master, self['bg'])
        newChatWindow.createWidgets(self['bg'], chatName, self.client, self)
        newChatListElement.bindMouseWheel( self.scrollableFrame)
        w =  self.master.winfo_screenwidth()*1.5/3
        newChatWindow.scrollableFrame.setCanvasWidth(w*3/4)
        newChatListElement.setElements(newChatWindow, chatName, lastMessage, timeString)

        index = len(self.chatListDict)
        self.chatListDict[chatName.lower()] = [newChatListElement, newChatWindow, index]
        self.scrollableFrame.update()
        self.scrollableFrame.canvas.yview_moveto( 1 )

    def receiveMessage(self, sender, message, time):
        if activeChat is not None and activeChat.chatName.get() == sender:
            self.chatListDict[activeChat.chatName.get().lower()][1].addBoxMessageElement(message, time, False)
        else:
            self.notify(sender, message, time, False, True, False)

    def notify(self, sender, message, time, isMine, notify, onLogin):
        searchKey = sender.lower()
        global activeChat
        if searchKey not in self.chatListDict:
            #chatList not found in the list
            self.addChatListElement(sender, message, time)
            self.client.startConnection(searchKey)
            if activeChat is None:
                # there is no active chat
                self.chatListDict[searchKey][0].changeChatRoom(event=None)
            if not onLogin:
                self.sortChatList(searchKey)
        elif not activeChat.chatName.get() == sender and notify == True:
            #there is an active chat but not the sender's one, so notify that
            self.chatListDict[searchKey][0].increaseNotifies(message, time)
            if not onLogin:
                self.sortChatList(searchKey)
        # add the new message to that chatWindow anyway
        self.chatListDict[searchKey][1].addBoxMessageElement(message, time, isMine)

    def updateMessageTime(self, chatName, message, time):
        searchKey = chatName.lower()
        self.chatListDict[searchKey][0].setLastMessage(message)
        self.chatListDict[searchKey][0].setLastMessageTime(time)

    def sortChatList(self, searchKey):
        oldIndex = self.chatListDict[searchKey][2]
        for key, val in self.chatListDict.items():
            if key == searchKey:
                val[2] = 0
            elif val[2] < oldIndex:
                val[2] += 1

        sortedByIndex = sorted(self.chatListDict.items(), key=lambda kv: kv[1][2])

        self.chatListDict = {}
        for cle in sortedByIndex:
            self.chatListDict[cle[0]] = [cle[1][0], cle[1][1], cle[1][2]]

        for cle in self.scrollableFrame.winfo_children():
            cle.pack_forget()

        for cle in sortedByIndex:
            self.scrollableFrame.winfo_children().append(cle[1][0])
            cle[1][0].pack(fill=X)
        self.scrollableFrame.update()

    def getNotEmptyUsers(self):
        list = []
        for cle in self.chatListDict.items():
            if not cle[1][0].lastMessageTime.get() == '-:--':
                list.append(cle[0])
        return list

    def flushChatDict(self):
        for cle in self.chatListDict.values():
            cle[0].destroy()
            cle[1].destroy()
        self.chatListDict = {}

class ChatListElement(Frame):
    MAXMESSAGELEN = 10

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
        global activeChat
        if  activeChat is None:
            activeChat = self.chatWindow
            activeChat.entryBar.focus_force()
            self.chatWindow.pack(side=RIGHT, fill=BOTH, expand=True)
            self.notifies.set(0)
            self.notifiesLabel.grid_forget()
        elif self.chatName.get() == activeChat.chatName.get():
            activeChat.pack_forget()
            activeChat.entryBar.focus_force()
            activeChat = None
        else:
            activeChat.pack_forget()
            activeChat = self.chatWindow
            activeChat.entryBar.focus_force()
            self.chatWindow.pack(side=RIGHT, fill=BOTH, expand=True)
            self.notifies.set(0)
            self.notifiesLabel.grid_forget()

    def createWidgets(self):
        self.photoLabel = Label(self, image = self.photo )
        self.chatNameLabel = Label(self, textvariable = self.chatName, background=self['bg'], fg='white', anchor=NW)
        self.lastMessageLabel = Label(self, textvariable = self.lastMessage, background=self['bg'], anchor=NW, fg='white')
        self.lastMessageTimeLabel = Label(self, textvariable = self.lastMessageTime, background=self['bg'],  anchor=NE, fg='white')
        self.notifiesLabel = Label(self, textvariable = self.notifies, background='#7070db' )

        self.photoLabel.grid(row=0, column=0, rowspan=2, sticky=W, padx=5, pady=5)
        self.chatNameLabel.grid(row=0, column=1, sticky=W+E, padx=5)
        self.lastMessageLabel.grid(row=1,column=1, sticky=W+E, padx=5)
        self.lastMessageTimeLabel.grid(row=0,column=2, sticky=W+E)

        self.bind('<Button-1>', self.changeChatRoom)
        self.chatNameLabel.bind('<Button-1>', self.changeChatRoom)
        self.lastMessageLabel.bind('<Button-1>', self.changeChatRoom)
        self.lastMessageTimeLabel.bind('<Button-1>', self.changeChatRoom)
        self.photoLabel.bind('<Button-1>', self.changeChatRoom)
        self.notifiesLabel.bind('<Button-1>', self.changeChatRoom)

    def checkStringLenght(self, s):
        if ( len(s) > self.MAXMESSAGELEN ):
            return s[0:self.MAXMESSAGELEN] + " ..."
        return s

    def bindMouseWheel(self, scrollableFrame):
        self.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.chatNameLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.lastMessageLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.lastMessageTimeLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.photoLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.notifiesLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)

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
