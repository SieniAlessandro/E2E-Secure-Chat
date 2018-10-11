from tkinter import *


class SignUpGUI(Tk):

    backgroundWindow = '#47476b'
    def __init__(self):
        Tk.__init__(self)
        w = 300 # width for the Tk root
        h = 450 # height for the Tk root
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.resizable(width=FALSE, height=FALSE)
        self.title("Sign Up")
        self.mainFrame = Frame(self, bg=self.backgroundWindow)
        self.titleLabel = Label(self.mainFrame, text="Sign Up", bg=self.backgroundWindow, font = ("Default", 18, "bold"), fg='white')
        self.usernameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.usernameEntry = Entry(self.mainFrame, validate="focus", vcmd= lambda: self.validate(self.usernameEntry), invalidcommand = lambda: self.invalidate(self.usernameEntry) )
        self.nameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Name")
        self.nameEntry = Entry(self.mainFrame,  validate="focus", vcmd= lambda: self.validate(self.nameEntry), invalidcommand = lambda: self.invalidate(self.nameEntry) )
        self.surnameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Surname")
        self.surnameEntry = Entry(self.mainFrame,  validate="focus", vcmd= lambda: self.validate(self.surnameEntry), invalidcommand = lambda: self.invalidate(self.surnameEntry) )
        self.passwordLabel = Label(self.mainFrame, text="Password", bg=self.backgroundWindow, fg='white')
        self.passwordEntry = Entry(self.mainFrame, show="*")
        self.buttonsFrame = Frame(self.mainFrame, bg=self.backgroundWindow   )
        self.cancelButton = Button(self.buttonsFrame, text="Cancel", command=self.cancelEvent)
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

    def validate(self, entry):
        return len(entry.get()) < 20

    def invalidate(self, entry):
        entry.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)

    def setLoginWindow(self, loginWindow):
        self.loginWindow = loginWindow

    def cancelEvent(self):
        self.usernameEntry.delete(0, 'end')
        self.nameEntry.delete(0, 'end')
        self.surnameEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.withdraw()
        self.loginWindow.deiconify()

# signUp = SignUpGUI()
#
# signUp.mainloop()
