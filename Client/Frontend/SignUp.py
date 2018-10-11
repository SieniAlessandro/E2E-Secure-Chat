from tkinter import *


class SignUpGUI(Tk):

    backgroundWindow = '#47476b'
    def __init__(self):
        Tk.__init__(self)
        self.geometry('300x450')
        self.resizable(width=FALSE, height=FALSE)
        self.title("Sign Up")
        self.mainFrame = Frame(self, bg=self.backgroundWindow)
        self.titleLabel = Label(self.mainFrame, text="Sign Up", bg=self.backgroundWindow, font = ("Default", 18, "bold"), fg='white')
        self.usernameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.usernameEntry = Entry(self.mainFrame)
        self.nameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Name")
        self.nameEntry = Entry(self.mainFrame)
        self.surnameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.surnameEntry = Entry(self.mainFrame)
        self.passwordLabel = Label(self.mainFrame, text="Password", bg=self.backgroundWindow, fg='white')
        self.passwordEntry = Entry(self.mainFrame, show="*")
        self.buttonsFrame = Frame(self.mainFrame, bg=self.backgroundWindow   )
        self.cancelButton = Button(self.buttonsFrame, text="Cancel")
        self.confirmButton = Button(self.buttonsFrame, text="Confirm")
        self.mainFrame.pack(fill=BOTH, expand=True)
        self.titleLabel.pack(pady=15)

        self.usernameLabel.pack(pady=5)
        self.usernameEntry.pack(pady=5)

        self.nameLabel.pack(pady=5)
        self.nameEntry.pack(pady=5)

        self.surnameLabel.pack(pady=5)
        self.surnameEntry.pack(pady=5)

        self.passwordLabel.pack(pady=5)
        self.passwordEntry.pack(pady=5)

        self.buttonsFrame.pack(side = BOTTOM, pady=10)
        self.cancelButton.pack(side="left", padx=5, pady=5)
        self.confirmButton.pack(side="right", padx=5, pady=5)


signUp = SignUpGUI()

signUp.mainloop()
