from tkinter import *
from PIL import ImageTk, Image

class LoginGUI(Frame):
    backgroundWindow = '#1f2327'
    backgroundItems = '#434d56'
    activebackground = '#657481'
    errorColor = '#ff3333'
    def __init__(self, master):
        """
            Login Grafic Interface, this is the first shown if the autologin is disabled

            :type master: Tk
            :param master: parent widget
        """
        Frame.__init__(self, master)

        self.var = IntVar()
        self.mainFrame = Frame(self, bg=self.backgroundWindow)

        self.titleLabel = Label(self.mainFrame, text="Login", bg=self.backgroundWindow, font = ("Default", 18, "bold"), fg='white')

        self.messageLabel = Label(self.mainFrame, bg=self.backgroundItems)

        self.usernameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.usernameEntry = Entry(self.mainFrame,bg=self.backgroundItems, fg='white', relief='flat' )
        self.passwordLabel = Label(self.mainFrame, text="Password", bg=self.backgroundWindow, fg='white')
        self.passwordEntry = Entry(self.mainFrame, show="*", bg=self.backgroundItems, fg='white', relief='flat')
        self.buttonsFrame = Frame(self.mainFrame, bg=self.backgroundWindow )
        self.rememberLoginCheckbutton = Checkbutton(self.mainFrame, variable = self.var, text="Autologin", bg=self.backgroundWindow, fg='#2a8c8c', activebackground=self.backgroundItems, activeforeground='#2a8c8c')
        self.signUpButton = Button(self.buttonsFrame, text="Sign Up", command=self.signUpEvent, bg=self.backgroundItems, fg='white', relief='flat', activebackground = self.activebackground, activeforeground='white')
        self.confirmButton = Button(self.buttonsFrame, text="Confirm", command=self.loginEvent, bg=self.backgroundItems, fg='white', relief='flat', activebackground = self.activebackground, activeforeground='white')

        self.mainFrame.pack(fill=BOTH, expand=True)
        self.mainFrame.columnconfigure(0, weight=100)
        self.titleLabel.grid( row=0, pady=15)
        self.usernameLabel.grid(row=2, pady=5)
        self.usernameEntry.grid(row=3, pady=5)
        self.passwordLabel.grid(row=4, pady=5)
        self.passwordEntry.grid(row=5, pady=5)
        self.rememberLoginCheckbutton.grid(row=6, pady=5)
        self.buttonsFrame.grid(row=7, pady=10)
        self.signUpButton.pack(side="left", padx=5, pady=5)
        self.confirmButton.pack(side="right", padx=5, pady=5)

        self.master.bind('<Return>', self.pressEnterEvent)
    def setRootSize(self, height):
        """
            Set width and height of root window

            :type height: int
            :param height: height of login frame
        """
        w = 300 # width for the Tk root
        h = height # height for the Tk root
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
    def showLoginFrame(self):
        """
            Display login interface inside the root window
        """
        self.pack(fill=BOTH, expand=True)
        self.setRootSize(350)
        self.master.resizable(width=FALSE, height=FALSE)
        self.master.title("Login")
        self.master.protocol("WM_DELETE_WINDOW", self.client.onClosing )
        self.usernameEntry.focus_force()
    def hideLoginFrame(self):
        """
            Hide login interface from the root window
        """
        self.pack_forget()
        self.usernameEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.usernameEntry.config(fg ='white', highlightthickness=0)
        self.passwordEntry.config(fg = 'white', highlightthickness=0)
        self.hideMessage()
    def setItems(self, client, chat, signUpWindow, online):
        """
            Receive client instance in order to call client's functions, signUp
            and chat instance in order to show/hide them

            :type client: Client
            :param client: instance of class Client

            :type chat: ChatGUI
            :param chat: instance of class ChatGUI

            :type signUpWindow: SignUpGUI
            :param signUpWindow: instance of class SignUpGUI

            :type online: int
            :param online: server status
        """
        self.client = client
        self.chat = chat
        self.signUpWindow = signUpWindow
        if online == -1:
            self.showMessage("Server Offline, please try again later!",  "#ff3333" )
            self.confirmButton.config(state=DISABLED)
            self.signUpButton.config(state=DISABLED)
    def signUpEvent(self):
        """
            When Sign Up button is pressed
        """
        self.hideLoginFrame()
        self.signUpWindow.showSignUpFrame()
    def loginEvent(self):
        """
            When Confirm button is pressed, it checks that fields are not empty
            and call the client.login(), showing error if it doesn't succed or
            showing chat if the user has been logged
        """
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        if not username or not password :
            self.confirmButton.config(fg = self.errorColor, highlightbackground=self.errorColor, highlightcolor=self.errorColor, highlightthickness=1)
        else:
            self.client.setAutoLogin(self.var.get(), username, password )
            ret = self.client.login(username, password)
            if  ret == 1:
                self.hideLoginFrame()
                self.usernameEntry.delete(0, 'end')
                self.passwordEntry.delete(0, 'end')
                self.chat.onLoginEvent(username)
            elif ret == 0:
                self.showError()
            elif ret == -1:
                self.showMessage("You are already logged in other device",  self.errorColor )
    def pressEnterEvent(self, event):
        """
            :type event: Event
            :param event: information about the event
        """
        self.loginEvent()
    def showError(self):
        """
            Show error label and set fields style to red
        """
        self.messageLabel.config(text="Username or Password is incorrect", fg = "#ff1a1a")
        self.messageLabel.grid(row = 1)
        self.usernameEntry.config(fg = self.errorColor, highlightbackground=self.errorColor, highlightcolor=self.errorColor, highlightthickness=1)
        self.passwordEntry.config(fg = self.errorColor, highlightbackground=self.errorColor, highlightcolor=self.errorColor, highlightthickness=1)
        self.setRootSize(370)
    def hideMessage(self):
        self.messageLabel.grid_forget()
        self.usernameEntry.config(fg = 'white', highlightbackground=self.errorColor, highlightcolor=self.errorColor, highlightthickness=0)
        self.passwordEntry.config(fg = 'white', highlightthickness=0)
        self.setRootSize(350)
    def showMessage(self, message, color):
        """
            Show a label to notify some event
            :type message: string
            :param message: message to be shown
        """
        self.messageLabel.config(text=message, fg = color)
        self.messageLabel.grid(row = 1)
        self.setRootSize(370)

#Testing purposes
if __name__ == '__main__':
    from client import Client
    import ctypes
    import os
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    if sys.platform.startswith('win'):
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    login = LoginGUI(root)
    client = Client(None)
    login.setItems(client, chat=None, signUpWindow=None, online=None)
    login.showLoginFrame()
    login.showError()
    login.hideMessage()
    login.showMessage("ciao", "green")
    root.mainloop()
