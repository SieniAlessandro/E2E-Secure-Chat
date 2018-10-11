from tkinter import *

class LoginGUI(Tk):

    backgroundWindow = '#47476b'
    def __init__(self):
        Tk.__init__(self)
        self.geometry('300x300')
        self.resizable(width=FALSE, height=FALSE)
        self.title("Login")
        self.mainFrame = Frame(self, bg=self.backgroundWindow)
        self.titleLabel = Label(self.mainFrame, text="Login", bg=self.backgroundWindow, font = ("Default", 18, "bold"), fg='white')
        self.usernameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.usernameEntry = Entry(self.mainFrame   )
        self.passwordLabel = Label(self.mainFrame, text="Password", bg=self.backgroundWindow, fg='white')
        self.passwordEntry = Entry(self.mainFrame, show="*")
        self.buttonsFrame = Frame(self.mainFrame, bg=self.backgroundWindow   )
        self.signUpButton = Button(self.buttonsFrame, text="Sign Up")
        self.confirmButton = Button(self.buttonsFrame, text="Confirm")

        # self.mainFrame.pack_propagate(False)
        self.mainFrame.pack(fill=BOTH, expand=True)
        self.titleLabel.pack(pady=15)
        self.usernameLabel.pack(pady=5)
        self.usernameEntry.pack(pady=5)
        self.passwordLabel.pack(pady=5)
        self.passwordEntry.pack(pady=5)
        self.buttonsFrame.pack(pady=5)
        self.signUpButton.pack(side="left", padx=5, pady=5)
        self.confirmButton.pack(side="right", padx=5, pady=5)


login = LoginGUI()

login.mainloop()
