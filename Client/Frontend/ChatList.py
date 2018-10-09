from tkinter import *
from PIL import ImageTk, Image
from Chat import chatWindow as cw

class ChatList(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.list = []
        self.grid(row=0, column=0, rowspan=2, sticky=N+S+W)

    #     vscrollbar = Scrollbar(self, orient=VERTICAL)
    #     vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
    #     canvas = Canvas(self, bd=0, highlightthickness=0, width=250,
    #                     yscrollcommand=vscrollbar.set, bg=background)
    #     canvas.pack(side=LEFT, fill='y', expand=TRUE)
    #     vscrollbar.config(command=canvas.yview)
    #
    #     # reset the view
    #     canvas.xview_moveto(0)
    #     canvas.yview_moveto(0)
    #
    #     # create a frame inside the canvas which will be scrolled with it
    #     self.interior = interior = Frame(canvas, bg=background)
    #     interior_id = canvas.create_window(0, 0, window=interior,
    #                                        anchor=NW)
    #
    # # track changes to the canvas and frame width and sync them,
    # # also updating the scrollbar
    # def _configure_interior(event):
    #     # update the scrollbars to match the size of the inner frame
    #     size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
    #     canvas.config(scrollregion="0 0 %s %s" % size)
    #     if interior.winfo_reqwidth() != canvas.winfo_width():
    #         # update the canvas's width to fit the inner frame
    #         canvas.config(width=interior.winfo_reqwidth())
    #     interior.bind('<Configure>', _configure_interior)
    #
    # def _configure_canvas(event):
    #     if interior.winfo_reqwidth() != canvas.winfo_width():
    #         # update the inner frame's width to fill the canvas
    #         canvas.itemconfigure(interior_id, width=canvas.winfo_width())
    #     canvas.bind('<Configure>', _configure_canvas)
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
