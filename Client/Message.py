import socket
import random
import threading
import os
from client import *
from threading import Thread
import json
from Log import *

class Message :
    """
        Handles all the Messages of the Conversation between the users
    """
    MSG_LEN = 2048
    #Constructor
    def __init__(self, Log) :
        """
            Initialize the Message Handler

            :type Log: Log
            :param Log: the Log
        """
        self.Conversations = {}
        self.Log = Log
        self.Log.log('Message Handler has been initialized!')


    def createMessageJson(self, text, time, sender, logout) :
        """
            Create the dictionary with the passed data
            :type text: String
            :param text: the text of the message
            :type time: String
            :param time: the moment when the message is sent
            :type sender: String
            :param sender: The sender of the message
            :type logout: Boolean
            :param logout: specify if it is a logout message or not
            :rtype: Dict
            :return:
                    msg['text'] = text
                    msg['time'] = time
                    msg['sender'] = sender
                    msg['logout'] = logout
        """
        msg = {}
        msg['text'] = text
        msg['time'] = time
        msg['sender'] = sender
        msg['logout'] = logout
        return json.dumps(msg)

    def addMessagetoConversations(self, user, text, time, whoSendIt) :
        """
            creates a dictionary from the passed data and inserts it in the
            Conversation from the local user and the passed user
            :type user: String
            :param user: the user relative to the active conversation
            :type text: String
            :param text: the text of the message
            :type time: String
            :param time: the moment when the message has been sent
            :type whoSendIt: Boolean
            :param whoSendIt: specify if the user send it or the local client send it
        """
        msg = {}
        msg['text'] = text
        msg['time'] = time
        msg['whoSendIt'] = whoSendIt
        self.Log.log('Added message to the conversation : ' + json.dumps(msg))

        if user not in self.Conversations.keys() :
            self.Conversations[user] = {}

        #index initialization needed if there is no keys in the dictionary
        index = '0'
        if index in self.Conversations[user].keys() :
            #put the index in the last position of the dictionary relative to
            #the conversation with the specified user
            index = int(list(self.Conversations[user].keys())[-1]) + 1

        self.Conversations[user][index] = {}
        self.Conversations[user][index] = msg


    def retrieveAllConversations(self) :
        """
            Used to get all the conversations
            :rtype: Dict
            :return: The dictionary containing all the conversations with all the users
                    Conversations[user][index][text]
                    Conversations[user][index][time]
                    Conversations[user][index][whoSendIt]
        """
        self.Log.log('All the conversations has been charged : ' + json.dumps(self.Conversations))
        return self.Conversations

    def retrieveConversation(self, user) :
        """
            Used to get the conversation with the specified user
            :type user: String
            :param user: the user of the wanted conversation
            :rtype: Dict or Int
            :return: 0 if that conversation does not exist, otherwise the dictionary containing all the conversations with all the users
                    Dict[index][text]
                    Dict[index][time]
                    Dict[index][whoSendIt]
        """
        if user in self.Conversations.keys():
            self.Log.log('Conversation with ' + user + ' has been find : ' + json.dumps(self.Conversations))
            return self.Conversations[user]
        return 0

    def saveConversations(self, username, ordinatedUserList = None) :
        """
            Save all the conversations in a ordinated way, if there is the
            ordinatedUserList, for the local client, passed as username

            :type username: String
            :param username: The local user
            :type ordinatedUserList: List or None
            :param ordinatedUserList: None if it is not present an ordinated list, otherwise List<String>
        """
        if ordinatedUserList is not None:
            tempConversations = self.Conversations
            self.Conversations = {}
            for cle in ordinatedUserList:
                searchKey = cle.lower()
                self.Conversations[searchKey] = tempConversations[searchKey]
        username = username.lower()
        with open("Local/conversations-" + username + ".json","w") as outfile:
            json.dump(self.Conversations, outfile)

    def loadConversations(self, username) :
        """
            load the conversations for the local user passed as username

            :type username: String
            :param username: the local user
        """
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
            #if there are no conversations initialize the dictionary
            self.Conversations = {}
