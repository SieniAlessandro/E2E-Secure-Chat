import socket
import random
import threading
from client import *
from threading import Thread
import json
from Log import *

class MessageHandler :
    MSG_LEN = 2048
    #Constructor
    def __init__(self) :
        print('Hi')

    def createMessageJson(text, time) :

        msg = {}
        msg['text'] = text
        msg['time'] = time

        return json.dumps(msg)
