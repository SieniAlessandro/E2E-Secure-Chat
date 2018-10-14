from tkinter import *
from validate_email import validate_email
import re

class SignUpGUI(Tk):

    backgroundWindow = '#47476b'
    def __init__(self):
        Tk.__init__(self)
        w = 390 # width for the Tk root
        h = 350 # height for the Tk root
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.resizable(width=FALSE, height=FALSE)
        self.title("Sign Up")
        self.mainFrame = Frame(self, bg=self.backgroundWindow)
        self.rightFrame = Frame(self.mainFrame, bg=self.backgroundWindow)
        self.leftFrame = Frame(self.mainFrame, bg=self.backgroundWindow)
        self.titleLabel = Label(self.mainFrame, text="Sign Up", bg=self.backgroundWindow, font = ("Default", 18, "bold"), fg='white')
        self.errorLabel = Label(self.mainFrame, text="Something went wrong!", fg = "#ff1a1a", bg="#8585ad")

        self.usernameLabel = Label(self.leftFrame, bg=self.backgroundWindow, fg='white', text="Username")
        self.usernameEntry = Entry(self.leftFrame, validate="focusout", vcmd= lambda: self.validateLength(self.usernameEntry, 20), invalidcommand = lambda: self.invalidate(self.usernameEntry) )

        self.emailLabel = Label(self.leftFrame, bg=self.backgroundWindow, fg='white', text="Email")
        self.emailEntry = Entry(self.leftFrame,  validate="focusout", vcmd= lambda: self.validateEmail(), invalidcommand = lambda: self.invalidate(self.emailEntry) )

        self.nameLabel = Label(self.leftFrame, bg=self.backgroundWindow, fg='white', text="Name")
        self.nameEntry = Entry(self.leftFrame,  validate="focusout", vcmd= lambda: self.validateLength(self.nameEntry, 45), invalidcommand = lambda: self.invalidate(self.nameEntry) )

        self.surnameLabel = Label(self.rightFrame, bg=self.backgroundWindow, fg='white', text="Surname")
        self.surnameEntry = Entry(self.rightFrame,  validate="focusout", vcmd= lambda: self.validateLength(self.surnameEntry, 45 ), invalidcommand = lambda: self.invalidate(self.surnameEntry) )

        self.passwordLabel = Label(self.rightFrame, text="Password", bg=self.backgroundWindow, fg='white')
        self.passwordEntry = Entry(self.rightFrame, show="*", validate="focus", vcmd= lambda: self.validatePassword(), invalidcommand = lambda: self.invalidate(self.passwordEntry) )

        self.confirmPasswordLabel = Label(self.rightFrame, text="Confirm Password", bg=self.backgroundWindow, fg='white')
        self.confirmPasswordEntry = Entry(self.rightFrame, show="*", validate="focus", vcmd= lambda: self.validateConfirmPassword(), invalidcommand = lambda: self.invalidate(self.confirmPasswordEntry) )

        self.cancelButton = Button(self.mainFrame, text="Cancel", command=self.cancelEvent)
        self.confirmButton = Button(self.mainFrame, text="Confirm", command=self.signUpEvent)

        self.mainFrame.pack(fill=BOTH, expand=True)
        self.mainFrame.columnconfigure(0, weight=100)
        self.titleLabel.grid(row=0, columnspan=2)
        self.leftFrame.grid(row=2, column=0, padx=15, pady=10)
        self.rightFrame.grid(row=2, column=1,padx=15, pady=10)

        self.usernameLabel.pack(pady=5)
        self.usernameEntry.pack(pady=5)

        self.emailLabel.pack(pady=5)
        self.emailEntry.pack(pady=5)

        self.nameLabel.pack(pady=5)
        self.nameEntry.pack(pady=5)

        self.surnameLabel.pack(pady=5)
        self.surnameEntry.pack(pady=5)

        self.passwordLabel.pack(pady=5)
        self.passwordEntry.pack(pady=5)

        self.confirmPasswordLabel.pack(pady=5)
        self.confirmPasswordEntry.pack(pady=5)

        self.cancelButton.grid(row=3, column=0, padx=15, pady=10)
        self.confirmButton.grid(row=3, column=1, padx=15, pady=10)

        self.isFormValid = {}
        self.isFormValid[self.usernameEntry.winfo_name] = False
        self.isFormValid[self.emailEntry.winfo_name] = False
        self.isFormValid[self.nameEntry.winfo_name] = False
        self.isFormValid[self.surnameEntry.winfo_name] = False
        self.isFormValid[self.passwordEntry.winfo_name] = False
        self.isFormValid[self.confirmPasswordEntry.winfo_name] = False

    def validatePassword(self):
        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$"
        if re.findall(pattern, self.passwordEntry.get()):
            self.passwordEntry.config(fg = "green", highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.isFormValid[self.passwordEntry.winfo_name] = True
            return True
        return False

    def validateConfirmPassword(self):
        if self.confirmPasswordEntry.get() == self.passwordEntry.get():
            self.confirmPasswordEntry.config(fg = "green", highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.isFormValid[self.confirmPasswordEntry.winfo_name] = True
            return True
        return False

    def validateEmail(self):
        if validate_email(self.emailEntry.get()):
            self.emailEntry.config(fg = "green", highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.isFormValid[self.emailEntry.winfo_name] = True
            return True
        return False

    def validateLength(self, entry, length):
        if len(entry.get()) > 0 and len(entry.get()) < length :
            entry.config(fg = "green", highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.isFormValid[entry.winfo_name] = True
            return True
        return False

    def invalidate(self, entry):
        entry.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)
        self.isFormValid[entry.winfo_name] = False

    def setLoginWindow(self, loginWindow):
        self.loginWindow = loginWindow

    def cancelEvent(self):
        self.usernameEntry.delete(0, 'end')
        self.nameEntry.delete(0, 'end')
        self.surnameEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.withdraw()
        self.loginWindow.deiconify()

    def setClient(self, client):
        self.client = client

    def signUpEvent(self):
        if False in self.isFormValid.values():
            self.confirmButton.config(fg = "red", highlightbackground="red", highlightcolor="red", highlightthickness=1)
        else:
            self.confirmButton.config(fg = "black",  highlightthickness=0)
            self.client.register(self.usernameEntry.get(), self.passwordEntry.get(), self.emailEntry.get(), self.nameEntry.get(), self.surnameEntry.get(), '0')
            self.cancelEvent()

    def showErrorLabel(self):
        self.errorLabel.grid(row = 1, columnspan=2)

    def hideErrorLabel(self):
        self.errorLabel.grid_forget()

# signUp = SignUpGUI()
#
# signUp.mainloop()
