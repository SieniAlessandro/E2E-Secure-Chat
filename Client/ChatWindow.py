from tkinter import *
from PIL import ImageTk, Image
import datetime
import random
from ScrollableFrame import *

class ChatWindow(Frame):
    backgroundWindow = '#1f2327'
    MAXMESSAGELEN = 250
    def __init__(self, master, background):
        Frame.__init__(self, master, background=self.backgroundWindow)

        self.chatName = StringVar()
        self.userState = StringVar()
        self.listBoxMessage = []
        self.rowconfigure(1, weight=8)
        Grid.columnconfigure(master, 1, weight=1)
        Grid.columnconfigure(master, 2, weight=4)

    def createWidgets(self, background, chatName, client, chatList ):
        self.chatName.set(chatName)
        self.client = client
        self.chatList = chatList

        inputBar = Frame(self, background=background,  padx=10, pady=10, highlightbackground="black", highlightcolor="black", highlightthickness=1)

        chatBar = Frame(self, bg = background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        chatNameLabel = Label(chatBar, textvariable=self.chatName, font = ( "Default", 10, "bold"), bg = background, fg='white')
        userStateLabel = Label(chatBar, textvariable=self.userState, font = ( "Default", 8, "italic"), bg = background, fg='white')
        mainFrame = Frame(self)
        self.scrollableFrame = Scrollable(mainFrame, self['bg'])

        chatBar.pack( side="top", fill=X, ipadx=5, ipady=4)
        chatNameLabel.grid(row=0, sticky=W, padx=10, pady=5)
        userStateLabel.grid(row=1, sticky=W, padx=10, pady=5)

        mainFrame.pack(fill=BOTH, expand=True)

        inputBar.pack(side="bottom", fill=X, ipadx=5, ipady=4)
        inputBar.columnconfigure(0, weight=15)
        inputBar.columnconfigure(1, weight=1)

        self.entryBar = Entry(inputBar, background=background, bd =0, fg='white')
        self.entryBar.grid(row=0, column=0, sticky=W+E)
        self.entryBar.bind('<Return>', self.pressEnterEvent )
        self.entryBar.bind('<Escape>', self.pressEscEvent)
        self.icon = ImageTk.PhotoImage(Image.open("Images/sendIcon.png").resize( (30,30), Image.ANTIALIAS ))
        sendButton = Button(inputBar, text="send", command=self.pressSendButton, bg=background, bd=0, activebackground='#787878', image=self.icon)
        sendButton.grid(row=0, column=1)
    def setClient(self, client):
        self.client = client
    def addBoxMessageElement(self, message, time, isMine):
        timeString = str(time).split('.')[0].split(' ')[1][:-3]
        boxMessage = BoxMessage(self.scrollableFrame, self['bg'])
        boxMessage.createWidgets( message, timeString , isMine)
        boxMessage.bindMouseWheel(self.scrollableFrame)
        self.listBoxMessage.append(boxMessage)
        self.chatList.updateMessageTime(self.chatName.get(), message, time)
        self.scrollableFrame.update()
        self.scrollableFrame.canvas.yview_moveto( 1 )
    def getChatName(self):
        return self.chatName.get()
    def pressSendButton(self):
        message = str(self.entryBar.get())
        if not message:
            return
        chunks = [message[i:i+self.MAXMESSAGELEN] for i in range(0, len(message), self.MAXMESSAGELEN)]
        for c in chunks:
            self.send(c)
        self.entryBar.delete(0, 'end')
    def pressEnterEvent(self, event):
        self.pressSendButton()
    def send(self, message):
        self.addBoxMessageElement(message, datetime.datetime.now(), True)
        status = self.client.sendClient(str(self.chatName.get().lower()), message)
        self.chatList.sortChatList(self.chatName.get().lower())
        print("SEND status: " + str(status))
        self.updateState(status)
    def pressEscEvent(self, event):
        self.chatList.searchBar.focus_force()
        self.chatList.chatListDict[self.chatName.get().lower()][0].changeChatRoom(event=None)
    def updateState(self, status):
        if status == 1:
            self.userState.set('Online')
        else:
            self.userState.set('Offline')

class BoxMessage(Frame):
    def __init__(self, master, background):
        Frame.__init__(self, master, padx=3, pady=3, bg=background )
        self.message = StringVar()
        self.arrivalTime = StringVar()
        self.isMine = True
        self.pack(fill='x')
    def createWidgets(self, message, arrivalTime, isMine):
        rowFrame = Frame(self)
        self.messageLabel = Message(rowFrame, aspect=250, textvariable=self.message, padx=5, pady=2, fg='white')
        self.arrivalTimeLabel = Label(rowFrame, textvariable=self.arrivalTime, padx=5, pady=2, fg='white')

        self.message.set(message)
        self.arrivalTime.set(arrivalTime)
        self.isMine = isMine

        self.messageLabel.grid(row=0, column=0, sticky=N+S+W)
        self.arrivalTimeLabel.grid(row=0, column=1, sticky=NE)

        backgroundMine = '#2a8c8c'
        backgroundIts = '#282e33'
        if isMine:
            rowFrame.pack(side='right', fill='x', padx=10, pady=5)
            rowFrame.configure(background=backgroundMine)
            self.messageLabel.configure(background=backgroundMine)
            self.arrivalTimeLabel.configure(background=backgroundMine)
        else:
            rowFrame.pack(side='left', fill='x', padx=10, pady=5)
            rowFrame.configure(background=backgroundIts)
            self.messageLabel.configure(background=backgroundIts)
            self.arrivalTimeLabel.configure(background=backgroundIts)
    def bindMouseWheel(self, scrollableFrame):
        self.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.messageLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
        self.arrivalTimeLabel.bind('<MouseWheel>', scrollableFrame._on_mousewheel)
