from tkinter import *
from ChatList import ChatList
from ChatWindow import *
from client import Client
import os

class ChatGUI(Tk):
    backgroundWindow = '#1f2327'
    backgroundItems = '#282e33'
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
        self.activeChat = ChatWindow(self, self.backgroundWindow)
        self.emptyFrame = Frame(self, background=self.backgroundWindow)
        self.emptyMessage = Label(self.emptyFrame, text="Select a chat to start a conversation", fg = 'white', bg='#4f5a63', padx=3, pady=3)
        self.emptyFrame.grid(row=0, column=1, sticky=N+S+W+E)
        self.emptyFrame.grid_propagate(FALSE)
        self.emptyFrame.configure(width=self.w*3/4)
        self.emptyFrame.update()
        self.emptyMessage.place( x = self.emptyFrame.winfo_width()/2, y = self.emptyFrame.winfo_height()/2-20)

    def createWidgets(self, client):
        self.client = client
        self.activeChat.createWidgets(self.backgroundItems, "", self.client, self.chatList)
        self.chatList.setItems(self.client, self.activeChat)
        self.chatList.scrollableFrame.setCanvasWidth(self.w*1/4)

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
        print("closing event")
        self.destroy()
        self.client.onClosing(list(self.chatList.chatListDict.keys()))

if __name__ == '__main__':
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    chat = ChatGUI()
    client = Client("", 6555)
    chat.createWidgets(client)

    chat.chatList.addChatListElement("Rododendro", "Oggi piove", None)
    # chat.chatWindow.receiveMessage("Rododendro", "Associated", "0:00")
    chat.mainloop()
