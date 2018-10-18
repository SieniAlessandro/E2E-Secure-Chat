from tkinter import *
from PIL import ImageTk, Image
import datetime
import random
from ScrollableFrame import *

class ChatWindow(Frame):
    def __init__(self, master, background):
        Frame.__init__(self, master, background=background)

        self.chatName = StringVar()
        self.listBoxMessage = []
        self.rowconfigure(1, weight=8)
        self.grid(row=0, column=1, sticky=N+S+W+E)


    def createWidgets(self, background, chatName, client, chatList ):
        self.chatName.set(chatName)
        self.client = client
        self.chatList = chatList

        inputBar = Frame(self, background=background,  padx=10, pady=10, highlightbackground="black", highlightcolor="black", highlightthickness=1)

        chatBar = Frame(self, bg = background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        chatNameLabel = Label(chatBar, textvariable=self.chatName, font = ( "Default", 10, "bold"), bg = background, fg='white')
        mainFrame = Frame(self)
        self.scrollableFrame = Scrollable(mainFrame, self['bg'])

        chatBar.pack( side="top", fill=X, ipadx=5, ipady=4)
        chatNameLabel.grid(row=0, sticky=W, padx=10, pady=5)

        mainFrame.pack(fill=BOTH, expand=True)

        inputBar.pack(side="bottom", fill=X, ipadx=5, ipady=4)
        inputBar.columnconfigure(0, weight=15)
        inputBar.columnconfigure(1, weight=1)

        self.entryBar = Entry(inputBar, background=background, bd =0, fg='white')
        self.entryBar.grid(row=0, column=0, sticky=W+E)
        self.entryBar.bind('<Return>', self.pressEnterEvent )
        self.icon = ImageTk.PhotoImage(Image.open("Images/sendIcon.png").resize( (30,30), Image.ANTIALIAS ))
        sendButton = Button(inputBar, text="send", command=self.pressSendButton, bg=background, bd=0, activebackground='#787878', image=self.icon)
        sendButton.grid(row=0, column=1)

    def addBoxMessageElement(self, message, time, isMine):
        timeString = str(time).split('.')[0].split(' ')[1][:-3]
        boxMessage = BoxMessage(self.scrollableFrame, self['bg'])
        boxMessage.createWidgets( message, timeString , isMine)
        self.listBoxMessage.append(boxMessage)
        self.scrollableFrame.update()
        self.scrollableFrame.canvas.yview_moveto( 1 )

    def changeChatRoom(self, chatName, fill):
        self.entryBar.focus_force()
        self.chatName.set(chatName)
        if len(self.listBoxMessage) > 0:
            for m in self.listBoxMessage:
                m.pack_forget()
            self.listBoxMessage.clear()
        if fill:
            """ fill is false if the conversation is loaded after login when messages loading
                is handled by chat.onLoginEvent """
            newConversation = self.client.Message.retrieveConversation(chatName)
            if not newConversation == 0 :
                for m in newConversation:
                    isMine = True if newConversation[m]['whoSendIt'] == 0 else False
                    self.addBoxMessageElement(newConversation[m]['text'], newConversation[m]['time'], isMine)

    def setClient(self, client):
        self.client = client

    def pressSendButton(self):
        message = str(self.entryBar.get())
        if not message:
            return
        self.addBoxMessageElement(message, datetime.datetime.now(), True)
        self.entryBar.delete(0, 'end')
        ret = self.client.sendClient(str(self.chatName.get()), message)
        self.chatList.updateMessageTime(self.chatName.get(), message, datetime.datetime.now())

    def pressEnterEvent(self, event):
        self.pressSendButton()

    def receiveMessage(self, sender, message, time):
        if str(self.chatName.get()) == sender:
            self.addBoxMessageElement(message, time, False)
        else:
            self.chatList.notify(sender, message, time)

class BoxMessage(Frame):
    def __init__(self, master, background):
        Frame.__init__(self, master, padx=3, pady=3, bg=background )
        self.message = StringVar()
        self.arrivalTime = StringVar()
        self.isMine = True
        self.pack(fill='x')

    def createWidgets(self, message, arrivalTime, isMine):
        rowFrame = Frame(self)
        messageLabel = Message(rowFrame, aspect=350, textvariable=self.message, padx=5, pady=2, fg='white')
        arrivalTimeLabel = Label(rowFrame, textvariable=self.arrivalTime, padx=5, pady=2, fg='white')

        self.message.set(message)
        self.arrivalTime.set(arrivalTime)
        self.isMine = isMine

        messageLabel.grid(row=0, column=0, sticky=N+S+W)
        arrivalTimeLabel.grid(row=0, column=1, sticky=NE)

        backgroundMine = '#7070db'
        backgroundIts = '#24248f'
        if isMine:
            rowFrame.pack(side='right', fill='x', padx=10, pady=5)
            rowFrame.configure(background=backgroundMine)
            messageLabel.configure(background=backgroundMine)
            arrivalTimeLabel.configure(background=backgroundMine)
        else:
            rowFrame.pack(side='left', fill='x', padx=10, pady=5)
            rowFrame.configure(background=backgroundIts)
            messageLabel.configure(background=backgroundIts)
            arrivalTimeLabel.configure(background=backgroundIts)
