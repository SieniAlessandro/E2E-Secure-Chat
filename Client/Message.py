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
    def __init__(self, Log) :
        self.Conversations = {}
        self.Log = Log
        self.Log.log('Message Handler has been initialized!')


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
        self.Log.log('Added message to the conversation : ' + json.dumps(msg))

        if user not in self.Conversations.keys() :
            self.Conversations[user] = {}

        index = '0'
        if index in self.Conversations[user].keys() :
            index = int(list(self.Conversations[user].keys())[-1]) + 1


        self.Conversations[user][index] = {}
        self.Conversations[user][index] = msg
        #print('Inserted message :' + json.dumps(msg) + ' from : ' + user)

    def retrieveAllConversations(self) :
        self.Log.log('All the conversations has been charged : ' + json.dumps(self.Conversations))
        return self.Conversations

    def retrieveConversation(self, user) :

        if user in self.Conversations.keys():
            #print('This is the conversation with ' + user + ' : ' + json.dumps(self.Conversations[user]))
            #print("END OF CONVERSATION")
            self.Log.log('Conversation with ' + user + ' has been find : ' + json.dumps(self.Conversations))
            return self.Conversations[user]
        return 0

    def saveConversations(self) :
        with open("conversations.json","w") as outfile:
            json.dump(self.Conversations, outfile)

    def loadConversations(self, username) :
        try :
            with open("conversations" + username + ".json","r") as input :
                self.Conversations = json.load(input)
        except :
            file = open("conversations" + username + ".json","w")
            file.close()
            self.Conversations = {}
