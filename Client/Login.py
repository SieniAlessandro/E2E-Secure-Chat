from tkinter import *
from PIL import ImageTk, Image
import os

class LoginGUI(Frame):

    backgroundWindow = '#1f2327'
    backgroundItems = '#434d56'
    activebackground = '#657481'
    errorColor = '#ff3333'
    def __init__(self, master):
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

        master.bind('<Return>', self.pressEnterEvent)
        self.usernameEntry.focus_force()
    def showLoginFrame(self):
        self.pack(fill=BOTH, expand=True)
        master = self._nametowidget(self.winfo_parent())

        w = 300 # width for the Tk root
        h = 350 # height for the Tk root
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        master.resizable(width=FALSE, height=FALSE)
        master.title("Login")
        master.protocol("WM_DELETE_WINDOW", self.client.onClosing )
    def hideLoginFrame(self):
        self.pack_forget()
        self.usernameEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.usernameEntry.config(fg ='white', highlightthickness=0)
        self.passwordEntry.config(fg = 'white', highlightthickness=0)
        self.hideMessage()
    def setItems(self, client, chat, signUpWindow, online):
        self.client = client
        self.chat = chat
        self.signUpWindow = signUpWindow
        if online == -1:
            self.showMessage("Server Offline, please try again later!",  "#ff3333" )
            self.confirmButton.config(state=DISABLED)
            self.signUpButton.config(state=DISABLED)
    def signUpEvent(self):
        self.hideLoginFrame()
        self.signUpWindow.showSignUpFrame()
    def loginEvent(self):
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
        self.loginEvent()
    def showError(self):
        self.messageLabel.config(text="Username or Password is incorrect", fg = "#ff1a1a")
        self.messageLabel.grid(row = 1)
        self.usernameEntry.config(fg = self.errorColor, highlightbackground=self.errorColor, highlightcolor=self.errorColor, highlightthickness=1)
        self.passwordEntry.config(fg = self.errorColor, highlightbackground=self.errorColor, highlightcolor=self.errorColor, highlightthickness=1)
    def hideMessage(self):
        self.messageLabel.grid_forget()
    def showMessage(self, message, color):
        self.messageLabel.config(text=message, fg = color)
        self.messageLabel.grid(row = 1)

if __name__ == '__main__':
    if os.getcwd().find("Client") == -1:
        os.chdir("Client")

    root = Tk()
    login = LoginGUI(root)
    login.setItems(client=None, chat=None)
    login.showLoginFrame()
    root.mainloop()
