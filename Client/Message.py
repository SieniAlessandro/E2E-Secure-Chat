import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *

class Message :
    MSG_LEN = 2048
    #Constructor
    def __init__(self) :
        print('Hi')
        self.Conversations = {}

    def createMessageJson(self, text, time) :

        msg = {}
        msg['text'] = text
        msg['time'] = time

        return json.dumps(msg)

    def addMessagetoConversations(self, user, text, time, whoSendIt) :
        '''
            whoSendIt = 1 if the user send it else the client send it
        '''
        msg = {}
        msg['text'] = text
        msg['time'] = time
        msg['whoSendIt'] = whoSendIt

        if user not in self.Conversations.keys() :
            self.Conversations[user] = []

        self.Conversations[user].append(msg)

    def retrieveConversation(self, user) :
        
        if user in self.Conversations.keys():
            return self.Conversations[user]
        return 0
