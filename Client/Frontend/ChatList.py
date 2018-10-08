from tkinter import *
import ChatListElement  as cle

class ChatList(Frame):

    def __init__(self, master, background):
        Frame.__init__(self, master, background=background)
        self.list = []

    #     vscrollbar = Scrollbar(self, orient=VERTICAL)
    #     vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
    #     canvas = Canvas(self, bd=0, highlightthickness=0, width=250,
    #                     yscrollcommand=vscrollbar.set, bg=background)
    #     canvas.pack(side=LEFT, fill='y', expand=TRUE)
    #     vscrollbar.config(command=canvas.yview)
    #
    #     # reset the view
    #     canvas.xview_moveto(0)
    #     canvas.yview_moveto(0)
    #
    #     # create a frame inside the canvas which will be scrolled with it
    #     self.interior = interior = Frame(canvas, bg=background)
    #     interior_id = canvas.create_window(0, 0, window=interior,
    #                                        anchor=NW)
    #
    # # track changes to the canvas and frame width and sync them,
    # # also updating the scrollbar
    # def _configure_interior(event):
    #     # update the scrollbars to match the size of the inner frame
    #     size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
    #     canvas.config(scrollregion="0 0 %s %s" % size)
    #     if interior.winfo_reqwidth() != canvas.winfo_width():
    #         # update the canvas's width to fit the inner frame
    #         canvas.config(width=interior.winfo_reqwidth())
    #     interior.bind('<Configure>', _configure_interior)
    #
    # def _configure_canvas(event):
    #     if interior.winfo_reqwidth() != canvas.winfo_width():
    #         # update the inner frame's width to fill the canvas
    #         canvas.itemconfigure(interior_id, width=canvas.winfo_width())
    #     canvas.bind('<Configure>', _configure_canvas)

    def addChatListElement(self, chatName, lastMessage, lastMessageTime):
        newChatListElement = cle.ChatListElement(self, self['bg']).setElements(chatName, lastMessage, lastMessageTime)
        self.list.append(newChatListElement)
        # print(newChatListElement.chatName)
