from tkinter import *
import ChatList  as cl
from Chat import InputBar
from Chat import chatWindow

backgroundWindow = '#47476b'
backgroundItems = '#29293d'
root = Tk()
root.title("Sneaky Chat")
root.configure(background='white')
root.geometry('1024x720')
root.resizable(width=FALSE, height=FALSE)

# root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=6)

root.rowconfigure(0,weight=4)
# root.rowconfigure(1,weight=1)

chatWindow = chatWindow(root, backgroundWindow)
chatWindow.createWidgets(backgroundItems, "Federico", "Ultimo accesso alle 17:00")

chatList = cl.ChatList(root, backgroundItems)
chatList.setChatWindow(chatWindow)

inputBar = InputBar(root, backgroundItems)
inputBar.setChatWindow(chatWindow)

chatList.addChatListElement("Federico","Ciao,come va?", "15:20")
chatList.addChatListElement("Giovanni","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Vittoria","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Filomena","a", "15:20")
chatList.addChatListElement("Rihanna","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Giggetto","Ciao, domani vengo a trovarti!", "15:20")
chatList.addChatListElement("Giggiabaffa","Ciao, domani vengo a trovarti!", "15:20")

root.mainloop()
