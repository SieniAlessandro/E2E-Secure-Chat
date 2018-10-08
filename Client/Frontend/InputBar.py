from tkinter import *
from PIL import ImageTk, Image


class InputBar(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background,  padx=10, pady=10)
        self.columnconfigure(0,weight=15)
        self.columnconfigure(1, weight=1)

        self.entryBar = Entry(self, background=background, bd=0, fg='white')
        self.entryBar.grid(row=0, column=0, sticky=W+E)

        self.sendButton = Button(self, text="send", command=self.sendMessage, bg=background, bd=0, activebackground='#787878')
        self.sendButton.grid(row=0, column=1)
        self.icon = ImageTk.PhotoImage(Image.open("sendIcon.png").resize( (30,30), Image.ANTIALIAS ))
        self.sendButton.configure(image=self.icon)

    def sendMessage(self):
        # crea un nuovo messaggio
        # mostralo nella chat
        print("Sending message...")
        # magherini.sendMessage(self.entryBar.get())
