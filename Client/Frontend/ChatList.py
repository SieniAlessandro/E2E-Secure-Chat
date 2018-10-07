from tkinter import *
import ChatListElement  as cle

class ChatList:

    def __init__(self, master):
        self.mainFrame = Frame(master)
        self.list = []


    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        newChatListElement = cle.ChatListElement(self.mainFrame).setElements(chatName, lastMessage, lastMessageTime)
        cle.ChatListElement(newChatListElement).pack()
        self.list.append(newChatListElement)
        print(self.list)

root = Tk()
chatList = ChatList(root)
chatList.addChatListElement("Federico", "alsiuhdiaushdiuashdiuashduiasuidhasuhduiash0", "15:20")
chatList.addChatListElement("GiggiaBaffa", "qweqwe", "15:20")

root.mainloop()
