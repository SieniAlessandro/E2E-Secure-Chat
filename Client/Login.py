from tkinter import *

class LoginGUI(Tk):

    backgroundWindow = '#47476b'
    def __init__(self):
        Tk.__init__(self)
        w = 300 # width for the Tk root
        h = 300 # height for the Tk root
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.focus_force()
        self.resizable(width=FALSE, height=FALSE)
        self.title("Login")
        self.mainFrame = Frame(self, bg=self.backgroundWindow)

        self.titleLabel = Label(self.mainFrame, text="Login", bg=self.backgroundWindow, font = ("Default", 18, "bold"), fg='white')

        self.invalidInputLabel = Label(self.mainFrame, text="Username or Password is incorrect", fg = "#ff1a1a", bg="#8585ad")

        self.usernameLabel = Label(self.mainFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.usernameEntry = Entry(self.mainFrame, validate="focus", vcmd= lambda: self.validateLength(self.usernameEntry, 20), invalidcommand = lambda: self.invalidate(self.usernameEntry) )
        self.passwordLabel = Label(self.mainFrame, text="Password", bg=self.backgroundWindow, fg='white')
        self.passwordEntry = Entry(self.mainFrame, show="*")
        self.buttonsFrame = Frame(self.mainFrame, bg=self.backgroundWindow )
        self.signUpButton = Button(self.buttonsFrame, text="Sign Up", command=self.signUpEvent)
        self.confirmButton = Button(self.buttonsFrame, text="Confirm", command=self.loginEvent)

        self.mainFrame.pack(fill=BOTH, expand=True)
        self.mainFrame.columnconfigure(0, weight=100)
        self.titleLabel.grid( row=0, pady=15)
        self.usernameLabel.grid(row=2, pady=5)
        self.usernameEntry.grid(row=3, pady=5)
        self.passwordLabel.grid(row=4, pady=5)
        self.passwordEntry.grid(row=5, pady=5)
        self.buttonsFrame.grid(row=6, pady=10)
        self.signUpButton.pack(side="left", padx=5, pady=5)
        self.confirmButton.pack(side="right", padx=5, pady=5)

        self.isFormValid = {}
        self.isFormValid[self.usernameEntry.winfo_name] = False
        self.isFormValid[self.passwordEntry.winfo_name] = True

    def validateLength(self, entry, length):
        if len(entry.get()) > 0 and len(entry.get()) < length :
            entry.config(fg = "green", highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.isFormValid[entry.winfo_name] = True
            return True
        return False

    def invalidate(self, entry):
        entry.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)
        self.isFormValid[entry.winfo_name] = False


    def setSignUpWindow(self, signUpWindow):
        self.signUpWindow = signUpWindow

    def setClient(self, client):
        self.client = client

    def signUpEvent(self):
        self.withdraw()
        self.signUpWindow.deiconify()

    def loginEvent(self):
        print(self.isFormValid)
        if False in self.isFormValid.values():
            self.confirmButton.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)
        else:
            # if self.client.login(self.usernameEntry.get(),self.passwordEntry.get()):
            #     self.withdraw()
            #     # chiamare funzione di chatGUI dopo il login
            # else:
            #     self.invalidInput()

            self.client.login(self.usernameEntry.get(),self.passwordEntry.get())

    def invalidInput(self):
        self.invalidInputLabel.grid(row = 1)
        self.usernameEntry.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)
        self.passwordEntry.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)

    def hideInvalidInput(self):
        self.invalidInputLabel.grid_forget()

# login = LoginGUI()
#
# login.mainloop()
