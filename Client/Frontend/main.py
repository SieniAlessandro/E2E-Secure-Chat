from tkinter import *
import ChatList  as cl
import InputBar as ib
import chatWindow as cw

backgroundWindow = '#47476b'
backgroundItems = '#29293d'
root = Tk()
root.title("Sneaky Chat")
root.configure(background=backgroundWindow)
root.geometry('1024x720')
root.resizable(width=FALSE, height=FALSE)

# root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=6)

root.rowconfigure(0,weight=4)
root.rowconfigure(1,weight=1)

chatList = cl.ChatList(root, backgroundItems)
chatList.grid(row=0, column=0, rowspan=2, sticky=N+S+W)

# chatWindow = cw.chatWindow(root)
# chatWindow.grid(row=0, column=1, sticky=N+W+E)

inputBar = ib.InputBar(root, backgroundItems)
inputBar.grid(row=1, column=1, sticky=S+W+E)

chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Federico","Ciao, domani vengo a trovarti!", "15:20")

root.mainloop()
