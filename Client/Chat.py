from tkinter import *
from ChatList import ChatList
from ChatWindow import *
from client import Client
import os

class ChatGUI(Tk):
    backgroundWindow = '#1f2327'
    backgroundItems = '#282e33'
    activebackground = '#657481'

    def __init__(self):
        Tk.__init__(self)

        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        self.w = ws*1.5/3 # width for the Tk root
        self.h = hs*2.5/4 # height for the Tk root

        x = (ws/2) - (self.w/2)
        y = (hs/2) - (self.h/2)

        self.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.title("MPS Chat")

        self.protocol("WM_DELETE_WINDOW", self.onCloseEvent )
        self.resizable(width=FALSE, height=FALSE)
        self.rowconfigure(0,weight=100)
        self.chatList = ChatList(self, self.backgroundItems)
        self.activeChat = None
        self.emptyFrame = Frame(self, background=self.backgroundWindow)
        self.emptyMessage = Label(self.emptyFrame, text="Select a chat to start a conversation", fg = 'white', bg='#4f5a63', padx=3, pady=3)
        self.orLabel = Label(self.emptyFrame, text="or",  fg = 'white', bg=self.backgroundWindow, padx=3, pady=3 )
        self.logoutButton = Button(self.emptyFrame, command=self.logout, text="Logout", bg='#4f5a63', fg='white', relief='flat', activebackground = self.activebackground, activeforeground='white')
        self.emptyFrame.grid(row=0, column=1, sticky=N+S+W+E)
        self.emptyFrame.grid_propagate(FALSE)
        self.emptyFrame.configure(width=self.w*3/4)
        self.emptyFrame.update()
        self.emptyMessage.place( x = self.emptyFrame.winfo_width()/2, y = self.emptyFrame.winfo_height()/2-30, anchor=CENTER)
        self.orLabel.place( x = self.emptyFrame.winfo_width()/2, y = self.emptyFrame.winfo_height()/2-0, anchor=CENTER)
        self.logoutButton.place( x = self.emptyFrame.winfo_width()/2, y = self.emptyFrame.winfo_height()/2+30, anchor=CENTER)

    def createWidgets(self, client, login):
        self.client = client
        self.login = login
        self.chatList.setItems(self.client)
        self.chatList.scrollableFrame.setCanvasWidth(self.w*1/4)

    def logout(self):
        self.login.deiconify()
        self.withdraw()
        self.client.logout(self.chatList.getNotEmptyUsers())

    def onLoginEvent(self, username):
        self.deiconify()
        self.title("MPS Chat - " + username)
        self.chatList.searchBar.focus_force()
        conversations = self.client.Message.retrieveAllConversations()
        for c in conversations.keys():
            for m in conversations[c]:
                isMine = True if conversations[c][m]['whoSendIt'] == 0 else False
                self.chatList.notify(c, conversations[c][m]['text'], conversations[c][m]['time'],isMine, False, True)

    def onCloseEvent(self):
        self.destroy()
        self.client.onClosing(self.chatList.getNotEmptyUsers())

if __name__ == '__main__':
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    chat = ChatGUI()
    client = Client("")
    # chat.createWidgets(client)

    chat.chatList.addChatListElement("Rododendro", "Oggi piove", None)
    # chat.chatWindow.receiveMessage("Rododendro", "Associated", "0:00")
    chat.mainloop()
