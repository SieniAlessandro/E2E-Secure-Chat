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
            self.Conversations[user] = {}

        index = 0
        if index in self.Conversations[user].keys() :
            index = list(self.Conversations[user])[-1] + 1

        self.Conversations[user][index] = {}
        self.Conversations[user][index] = msg
        print('Inserted message :' + json.dumps(msg) + ' from : ' + user)

    def retrieveAllConversations(self) :
        return self.Conversations

    def retrieveConversation(self, user) :

        if user in self.Conversations.keys():
            print('This is the conversation with ' + user + ' : ' + json.dumps(self.Conversations[user]))
            print("END OF CONVERSATION")
            return self.Conversations[user]
        return 0

    def saveConversations(self) :
        file = open("conversations.txt","w")
        file.write(json.dumps(self.Conversations))
        file.close()

    def loadConversations(self) :
        file = open("conversation.txt","r")
        self.Conversations = json.loads(file.read())
        file.close()
