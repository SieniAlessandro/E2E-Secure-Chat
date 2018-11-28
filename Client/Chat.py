from tkinter import *
from ChatList import ChatList
from ChatWindow import *
from client import Client

class ChatGUI(Frame):
    """
        Chat Grafic Interface, creates widgets and handles several events
    """
    backgroundWindow = '#1f2327'
    backgroundItems = '#282e33'
    activebackground = '#657481'

    def __init__(self, master):
        """
            :type master: Tk
            :param master: parent widget
        """
        Frame.__init__(self, master)

        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen

        self.w = ws*1.5/3 # width for the Tk root
        self.h = hs*2.5/4 # height for the Tk root

        self.x = (ws/2) - (self.w/2)
        self.y = (hs/2) - (self.h/2)

        emptyFrameWidth = (self.w*3/4)/2
        emptyFrameHeight = self.h/2

        self.rowconfigure(0,weight=100)
        self.chatList = ChatList(self, self.backgroundItems)
        self.activeChat = None
        self.emptyFrame = Frame(self, background=self.backgroundWindow)
        self.emptyMessage = Label(self.emptyFrame, text="Select a chat to start a conversation", fg = 'white', bg='#4f5a63', padx=3, pady=3)
        self.orLabel = Label(self.emptyFrame, text="or",  fg = 'white', bg=self.backgroundWindow, padx=3, pady=3 )
        self.logoutButton = Button(self.emptyFrame, command=self.logout, text="Logout", bg='#4f5a63', fg='white', relief='flat', activebackground = self.activebackground, activeforeground='white')
        self.emptyFrame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.emptyFrame.pack_propagate(FALSE)
        self.emptyFrame.update()
        self.emptyMessage.place( x =emptyFrameWidth, y = emptyFrameHeight-30, anchor=CENTER)
        self.orLabel.place( x =emptyFrameWidth, y = emptyFrameHeight-0, anchor=CENTER)
        self.logoutButton.place( x =emptyFrameWidth, y = emptyFrameHeight+30, anchor=CENTER)
    def createWidgets(self, client, login):
        """
            Receive client instance in order to call client's functions, login instance in order to show/hide the login window

            :type client: Client
            :param client: instance of class Client

            :type login: LoginGUI
            :param login: instance of class LoginGUI
        """
        self.client = client
        self.login = login
        self.chatList.setItems(self.client)
        self.chatList.scrollableFrame.setCanvasWidth(self.w*1/4)
    def logout(self):
        """
            Call client logout function and swap windows
        """
        self.client.logout(self.chatList.getNotEmptyUsers())
        self.login.showLoginFrame()
        self.hideChatFrame()
    def onLoginEvent(self, username):
        """
            After login, change window and load all the previous conversation + the new conversation received from the server

            :type username: string
            :param username: logged in username
        """
        self.showChatFrame()
        master = self._nametowidget(self.winfo_parent())
        master.title("MPS Chat - " + username)
        self.chatList.searchBar.focus_force()
        conversations = self.client.Message.retrieveAllConversations()
        for c in conversations.keys():
            for m in conversations[c]:
                isMine = True if conversations[c][m]['whoSendIt'] == 0 else False
                self.chatList.notify(c, conversations[c][m]['text'], conversations[c][m]['time'],isMine, True)
    def onCloseEvent(self):
        """
            Deallocate resource window and call onClosing event of client in order to save locally the conversations
        """
        self.destroy()
        self.client.onClosing(self.chatList.getNotEmptyUsers())
    def showChatFrame(self):
        """
            Display chat interface inside the root window
        """
        self.pack(fill=BOTH, expand=True)
        master = self._nametowidget(self.winfo_parent())
        master.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        master.title("MPS Chat")
        master.resizable(width=FALSE, height=FALSE)
        master.protocol("WM_DELETE_WINDOW", self.onCloseEvent )
    def hideChatFrame(self):
        """
            Hide chat interface from the root window
        """
        self.pack_forget()
        self.chatList.flushChatDict()

# Testing purposes
if __name__ == '__main__':
    import ctypes
    import os
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    root = Tk()
    chat = ChatGUI(root)
    client = Client()
    chat.createWidgets(client, None)
    if sys.platform.startswith('win'):
            ctypes.windll.shcore.SetProcessDpiAwareness(1)

    chat.chatList.addChatListElement("Rododendro", "Oggi piove", None)
    chat.showChatFrame()
    root.mainloop()
