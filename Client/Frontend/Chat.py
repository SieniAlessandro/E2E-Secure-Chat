from tkinter import *
from PIL import ImageTk, Image
import datetime
import random

class InputBar(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background,  padx=10, pady=10, highlightbackground="black", highlightcolor="black", highlightthickness=1)

        self.grid(row=1, column=1, sticky=S+W+E)
        self.columnconfigure(0, weight=15)
        self.columnconfigure(1, weight=1)

        self.entryBar = Entry(self, background=background, bd=0, fg='white')
        self.entryBar.grid(row=0, column=0, sticky=W+E)
        self.entryBar.bind('<Return>', self.pressEnterEvent )
        self.sendButton = Button(self, text="send", command=self.pressSendButton, bg=background, bd=0, activebackground='#787878')
        self.sendButton.grid(row=0, column=1)
        self.icon = ImageTk.PhotoImage(Image.open("Client/Frontend/sendIcon.png").resize( (30,30), Image.ANTIALIAS ))
        self.sendButton.configure(image=self.icon)

    def setChatWindow(self, chatWindow ):
        self.chatWindow = chatWindow

    def pressSendButton(self):
        message = self.entryBar.get()
        if not message:
            return
        self.chatWindow.addBoxMessageElement(self.entryBar.get())

        self.entryBar.delete(0, 'end')
        print("Sending message...")
        # magherini.sendMessage(self.entryBar.get())

    def pressEnterEvent(self, event):
        self.pressSendButton()


class chatWindow(Frame):
    def __init__(self, master, background):
        Frame.__init__(self, master, background=background)

        self.chatName = StringVar()
        self.listMessage = []
        self.rowconfigure(1, weight=8)
        self.grid(row=0, column=1, sticky=N+S+W+E)

    def updateCanvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def createWidgets(self, background, chatName ):
        self.chatName.set(chatName)
        self.canvas = Canvas(self,  highlightbackground="yellow", highlightcolor="yellow", highlightthickness=2)
        self.canvasFrame = Frame(self.canvas, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        self.canvasFrame.columnconfigure(0, weight=30)
        self.canvasFrame.columnconfigure(1, weight=40)
        self.canvasFrame.columnconfigure(2, weight=30)

        verticalScrollbar = Scrollbar(self.canvasFrame, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=verticalScrollbar.set)

        chatBar = Frame(self, height=50, bg = background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        chatNameLabel = Label(chatBar, textvariable=self.chatName, font = ( "Default", 10, "bold"), bg = background, fg='white')
        chatBar.pack( side="top", fill=X)
        chatNameLabel.grid(row=0, sticky=W, padx=10, pady=5)

        # verticalScrollbar.pack(side="right", fill="y", expand=True)
        self.canvas.grid_propagate(False)
        self.canvas.columnconfigure(0, weight=10)
        self.canvasFrame.grid(column=0, sticky=N+S+W+E)
        verticalScrollbar.grid(column = 1, sticky=N+S)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self.canvasFrame, anchor='nw')
        self.canvasFrame.bind("<Configure>", self.updateCanvas)
        print(self.canvas.grid_size())

    def addBoxMessageElement(self, message):
        timeString = str(datetime.datetime.now()).split('.')[0].split(' ')[1][:-3]
        boxMessage = BoxMessage(self.canvasFrame)
        boxMessage.createWidgets( message, timeString , random.choice([True, False]))
        self.listMessage.append(boxMessage)

    def changeChatRoom(self, chatName):
        self.chatName.set(chatName)
        print(self.listMessage)
        if len(self.listMessage) > 0:
            for m in self.listMessage:
                m.grid_forget()
            self.listMessage.clear()

class BoxMessage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, padx=3, pady=3)
        self.message = StringVar()
        self.arrivalTime = StringVar()
        self.isMine = True

        self.columnconfigure(0, weight=20)
        self.columnconfigure(1, weight=1)

    def createWidgets(self, message, arrivalTime, isMine):
        messageLabel = Message(self, aspect=350, textvariable=self.message, padx=5, pady=2, fg='white')
        arrivalTimeLabel = Label(self, textvariable=self.arrivalTime, padx=5, pady=2, fg='white')

        self.message.set(message)
        self.arrivalTime.set(arrivalTime)
        self.isMine = isMine

        messageLabel.grid(row=0, column=0, sticky=N+S+W)
        arrivalTimeLabel.grid(row=0, column=1, sticky=NE)

        backgroundMine = '#7070db'
        backgroundIts = '#24248f'
        if isMine:
            self.grid(column=2, sticky=E, padx=10, pady=5)
            self.configure(background=backgroundMine)
            messageLabel.configure(background=backgroundMine)
            arrivalTimeLabel.configure(background=backgroundMine)
        else:
            self.grid(column=0, sticky=W, padx=10, pady=5)
            self.configure(background=backgroundIts)
            messageLabel.configure(background=backgroundIts)
            arrivalTimeLabel.configure(background=backgroundIts)
