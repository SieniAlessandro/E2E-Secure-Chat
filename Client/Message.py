import socket
import random
import threading
import os
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


    def createMessageJson(self, text, time, sender = 'None') :

        msg = {}
        msg['text'] = text
        msg['time'] = time
        msg['sender'] = sender
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

    def saveConversations(self, username, ordinatedUserList) :
        tempConversations = self.Conversations
        self.Conversations = {}
        for cle in ordinatedUserList:
            searchKey = cle.lower()
            self.Conversations[searchKey] = tempConversations[searchKey]
        username = username.lower()
        with open("Local/conversations-" + username + ".json","w") as outfile:
            json.dump(self.Conversations, outfile)

    def loadConversations(self, username) :
        username = username.lower()
        try :
            with open("Local/conversations-" + username + ".json","r") as input :
                self.Conversations = json.load(input)
        except Exception as e :
            try:
                os.stat("Local")
            except:
                os.mkdir("Local")
            print("created file for the backup of the conversations of " + username)
            file = open("Local/conversations-" + username + ".json","w")
            file.close()
            self.Conversations = {}
