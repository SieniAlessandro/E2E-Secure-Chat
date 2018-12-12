from tkinter import *
from PIL import ImageTk, Image
from ChatWindow import *
from ScrollableFrame import *

activeChat = None

class ChatList(Frame):
    MAXSEARCHLEN = 20
    def __init__(self, master, background):
        """
            :type master: ChatGUI
            :param master: parent widget

            :type background: string
            :param background: background color
        """
        Frame.__init__(self, master, background=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.chatListDict = {}
        self.master = master

        self.pack(side=LEFT,fill=BOTH)
        self.searchBarFrame = Frame(self, bg=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        listFrame = Frame(self)
        self.scrollableFrame = Scrollable(listFrame, background)
        validation = self.register(self.checkEntryLength)
        self.searchBar = Entry(self.searchBarFrame, validate = "key", validatecommand = (validation, '%d'), background=background, bd=0, fg='white')
        self.searchBar.bind('<Return>', self.pressEnterEvent )
        self.searchIcon = ImageTk.PhotoImage(Image.open("Images/searchIcon.png").resize( (30,30), Image.ANTIALIAS ))
        self.searchButton = Button(self.searchBarFrame, text="search", command=self.pressSearchButton, bg=background, bd=0, activebackground='#787878', image=self.searchIcon)

        self.searchBarFrame.pack(side="top", fill=X)
        self.searchBar.pack(side=LEFT, padx=5,pady=5)
        self.searchButton.pack(side=RIGHT, padx=5, pady=5)
        listFrame.pack(fill=BOTH, expand=True)

    def pressSearchButton(self):
        """
            When search button is pressed, it checks if the chat already exists
            and it open that chat if exists. Else starts a connection with the
            searched name calling client.startConnection. If this function succedes
            it creates a new chat element and add it into the dictionary using
            the chat name as key, otherwise it invalidates the entry
        """
        username = self.searchBar.get()
        searchKey = username.lower()
        if not username:
            return
        if searchKey not in self.chatListDict:
            status = self.client.startConnection(searchKey)
            if status >= 0:
                self.addChatListElement(username, "", lastMessageTime=None)
                self.searchBarFrame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
                self.searchBar.config(fg='white')
                self.searchBar.delete(0, 'end')
                self.chatListDict[searchKey][1].updateState(status)
            else:
                self.searchBarFrame.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.searchBar.config(fg='red')
        else:
            self.chatListDict[searchKey][0].changeChatWindow(event=None)
    def checkEntryLength(self, action):
        """
            :rtype: boolean
            :return: the length of entry's string cannot exceed MAXSEARCHLEN
        """
        if action != '0' and len(self.searchBar.get()) >= self.MAXSEARCHLEN:
            return False
        return True
    def pressEnterEvent(self, event):
        """
            :type event: Event
            :param event: information about the event
        """
        self.pressSearchButton()
    def setItems(self, client ):
        """
            :type client: Client
            :param client: instance of class Client
        """
        self.client = client
    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        """
            Creates a new chatListElement and adds it to the dictionary

            :type chatName: string
            :param chatName: name of the chatListElement

            :type lastMessage: string
            :param lastMessage: last arrived or sent message

            :type lastMessageTime: string
            :param lastMessageTime: time of the last arrived or sent message
        """
        global activeChat
        if lastMessageTime is None:
            timeString = '-:--'
        else:
            timeString = str(lastMessageTime).split('.')[0].split(' ')[1][:-3]

        newChatListElement = ChatListElement(self.scrollableFrame, self['bg'])
        newChatListElement.setChatList(self)
        newChatListElement.createWidgets()

        newChatWindow = ChatWindow(self.master, self['bg'])
        newChatWindow.createWidgets(self['bg'], chatName, self.client, self)
        newChatListElement.bindMouseWheel( self.scrollableFrame)

        w =  self.master.winfo_screenwidth()*1.5/3
        newChatWindow.scrollableFrame.setCanvasWidth(w*3/4)
        newChatListElement.setElements(newChatWindow, chatName, lastMessage, timeString)

        index = len(self.chatListDict)
        self.chatListDict[chatName.lower()] = [newChatListElement, newChatWindow, index]
        if activeChat is None:
            # there is no active chat
            self.chatListDict[chatName.lower()][0].changeChatWindow(event=None)

        self.scrollableFrame.update()
        self.scrollableFrame.canvas.yview_moveto( 1 )
    def notify(self, sender, message, time, isMine, onLogin):
        """
            When a message is received, if the sender is not in dict create a new
            chatListElement and starts the connection with the sender. If the
            chatListElement is already in the dict, if the activeChat is not the
            sender's one, then increment the number of unreaded messages of the
            sender. In any case, add the boxMessageElement to the sender chat

            :type sender: string
            :param sender: name of the sender

            :type message: string
            :param message: sent or received message

            :type time: string
            :param time: arrival or sending time

            :type isMine: boolean
            :param isMine: true if this is a message sent by me

            :type onLogin: boolean
            :param onLogin: true if this is called after the login to restore chats
        """
        global activeChat
        searchKey = sender.lower()
        if searchKey not in self.chatListDict:
            #chatList not found in the list
            self.addChatListElement(sender, message, time)
            status = self.client.startConnection(searchKey)
            self.chatListDict[searchKey][1].updateState(status)
            if not onLogin:
                self.sortChatList(searchKey)
        elif searchKey in self.chatListDict and activeChat is None:
            self.chatListDict[searchKey][0].changeChatWindow()
        elif activeChat is not None and not activeChat.chatName.get() == sender and onLogin == False:
            #there is an active chat but not the sender's one, so notify that
            self.chatListDict[searchKey][0].increaseNotifies(message, time)
            self.chatListDict[searchKey][1].updateState(1)
            self.sortChatList(searchKey)
        elif activeChat is not None and activeChat.chatName.get() == sender and onLogin == False:
            self.chatListDict[searchKey][1].updateState(1)

        # add the new message to that chatWindow anyway
        self.chatListDict[searchKey][1].addBoxMessageElement(message, time, isMine)
    def updateMessageTime(self, chatName, message, time):
        """
            Every time a new message is received or sent, it updates the last
            message of the chat list element

            :type chatName: string
            :param chatName: name of the chat

            :type message: string
            :param message: sent or received message

            :type time: string
            :param time: arrival or sending time
        """
        searchKey = chatName.lower()
        self.chatListDict[searchKey][0].setLastMessage(message)
        self.chatListDict[searchKey][0].setLastMessageTime(time)
    def sortChatList(self, searchKey):
        """
            bring the chat with chatname==searchKey in the first row of the list.
            The list is sorted by the last message time so the higher the element
            is in the list, the more recent the last message is

            :type searchKey: string
            :param searchKey: name of the chat in the dictionary
        """
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
        """
            create a list of chat names with atleast one message sent or received

            :rtype: list
            :return: list of chat name
        """
        list = []
        for cle in self.chatListDict.items():
            if not cle[1][0].lastMessageTime.get() == '-:--':
                list.append(cle[0])
        return list
    def flushChatDict(self):
        """
            Destroy all the chat of the list
        """
        for cle in self.chatListDict.values():
            cle[0].destroy()
            cle[1].destroy()
        self.chatListDict = {}
    def deleteChatListElement(self, username):
        """
            Delete the chat list element

            :type username: string
            :param username: name of the chat to be deleted
        """
        global activeChat
        username = username.lower()
        if activeChat is not None and activeChat.chatName.get() == self.chatListDict[username][1].chatName.get():
            activeChat = None

        self.chatListDict[username][0].destroy()
        self.chatListDict[username][1].destroy()
        indexToRemove = self.chatListDict[username][2]
        del self.chatListDict[username]

        for key, val in self.chatListDict.items():
            if val[2] > indexToRemove:
                val[2] -= 1

class ChatListElement(Frame):
    MAXMESSAGELEN = 10

    def __init__(self, master, background):
        """
            Element of the list on left side of the chat

            :type master: Scrollable
            :param master: parent widget

            :type background: string
            :param background: background color
        """

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
    def createWidgets(self):
        """
            Creates widgets inside the chat list element and binds the click
            event in order to change the chat on click and the right-click in
            order to display the menu and select "delete"
        """
        self.rightClickMenu = Menu(self, tearoff=0)
        self.rightClickMenu.add_command(label="Delete", command= lambda: self.chatList.deleteChatListElement(self.chatName.get()))

        self.photoLabel = Label(self, image = self.photo )
        self.chatNameLabel = Label(self, textvariable = self.chatName, background=self['bg'], fg='white', anchor=NW)
        self.lastMessageLabel = Label(self, textvariable = self.lastMessage, background=self['bg'], anchor=NW, fg='white')
        self.lastMessageTimeLabel = Label(self, textvariable = self.lastMessageTime, background=self['bg'],  anchor=NE, fg='white')
        self.notifiesLabel = Label(self, textvariable = self.notifies, background='#7070db' )

        self.photoLabel.grid(row=0, column=0, rowspan=2, sticky=W, padx=5, pady=5)
        self.chatNameLabel.grid(row=0, column=1, sticky=W+E, padx=5)
        self.lastMessageLabel.grid(row=1,column=1, sticky=W+E, padx=5)
        self.lastMessageTimeLabel.grid(row=0,column=2, sticky=W+E)

        self.bind('<Button-1>', self.changeChatWindow)
        self.chatNameLabel.bind('<Button-1>', self.changeChatWindow)
        self.lastMessageLabel.bind('<Button-1>', self.changeChatWindow)
        self.lastMessageTimeLabel.bind('<Button-1>', self.changeChatWindow)
        self.photoLabel.bind('<Button-1>', self.changeChatWindow)
        self.notifiesLabel.bind('<Button-1>', self.changeChatWindow)

        if sys.platform.startswith('darwin'):
            self.bind('<Button-2>', self.popup)
            self.chatNameLabel.bind('<Button-2>', self.popup)
            self.lastMessageLabel.bind('<Button-2>', self.popup)
            self.lastMessageTimeLabel.bind('<Button-2>', self.popup)
            self.photoLabel.bind('<Button-2>', self.popup)
            self.notifiesLabel.bind('<Button-2>', self.popup)
        else:
            self.bind('<Button-3>', self.popup)
            self.chatNameLabel.bind('<Button-3>', self.popup)
            self.lastMessageLabel.bind('<Button-3>', self.popup)
            self.lastMessageTimeLabel.bind('<Button-3>', self.popup)
            self.photoLabel.bind('<Button-3>', self.popup)
            self.notifiesLabel.bind('<Button-3>', self.popup)
    def changeChatWindow(self, event=None):
        """
            When the element is clicked, it loads on the right frame, the clicked
            element's chatWindow

            :type event: Event
            :param event: information about the event
        """
        global activeChat
        if activeChat is None:
            activeChat = self.chatWindow
            activeChat.entryBar.focus_force()
            activeChat.pack(side=RIGHT, fill=BOTH, expand=True)
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
    def setChatList(self, chatList):
        """
            :type chatList: ChatList
            :param ChatListGUI: instance of class ChatList
        """
        self.chatList = chatList
    def popup(self, event):
        """
            Handles the right click event

            :type event: Event
            :param event: information about the event
        """
        try:
            self.rightClickMenu.tk_popup(event.x_root+40, event.y_root+10, 0)
        finally:
            self.rightClickMenu.grab_release()
    def checkStringLenght(self, s):
        """
            if the message is too long, it is cut and "..." is concatenated to it

            :type s: string
            :param s: string to be checked
        """
        if ( len(s) > self.MAXMESSAGELEN ):
            return s[0:self.MAXMESSAGELEN] + " ..."
        return s
    def bindMouseWheel(self, scrollableFrame):
        """
            Mouse wheel event

            :type scrollableFrame: Scrollable
            :param scrollableFrame: instance of class Scrollable
        """
        self.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.chatNameLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.lastMessageLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.lastMessageTimeLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.photoLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.notifiesLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
    def setLastMessage(self, message):
        """
            :type message: string
            :param message: last message
        """
        self.lastMessage.set(self.checkStringLenght(message))
    def setChatName(self, chatName):
        """
            :type chatName: string
            :param chatName: name of the chat
        """
        self.chatName.set(self.checkStringLenght(chatName))
    def setLastMessageTime(self, lastMessageTime):
        """
            :type lastMessageTime: string
            :param lastMessageTime: time of the last arrived or sent message
        """
        timeString = str(lastMessageTime).split('.')[0].split(' ')[1][:-3]
        self.lastMessageTime.set(timeString)
    def setElements(self, chatWindow, chatName, lastMessage, lastMessageTime):
        """
            :type chatWindow: ChatWindow
            :param chatWindow: instance of class ChatWindow

            :type chatName: string
            :param chatName: name of the chat

            :type lastMessage: string
            :param lastMessage: last message

            :type lastMessageTime: string
            :param lastMessageTime: time of the last arrived or sent message
        """
        self.chatWindow = chatWindow
        self.chatName.set(self.checkStringLenght(chatName))
        self.lastMessage.set(self.checkStringLenght(lastMessage))
        self.lastMessageTime.set(lastMessageTime)
    def increaseNotifies(self, message, time):
        """
            Display the notify label and add 1 to the variable

            :type message: string
            :param message: last message

            :type time: string
            :param time: time of the last arrived message
        """
        self.notifies.set(self.notifies.get()+1)
        self.notifiesLabel.grid(row=1, column=2, sticky=W+E)
        self.setLastMessage(message)
        self.setLastMessageTime(time)
