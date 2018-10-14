import pymysql
class Database:

    """This class is able to manage the connection with the database"""

    #In the init function the class try to establish a connection with the database, in order to allows
    #the programmer to modify the information stored in the database using the methods offered by this class

    def __init__(self,_host,_port,_user,_password,_db):
        #Establishing the connection with the database
        #self.db = pymysql.connect(host='localhost', port=3306, user='root', passwd='rootroot', db='messaggistica_mps')
        self.db = pymysql.connect(host=_host, port=_port, user=_user, passwd=_password, db=_db)
        #Creating a cursor useful to execute the desired query
        self.cursor = self.db.cursor()


    def insert_user(self,user,password,name,surname,email,key):
        """This method allows us to insert a new user a is invoked when a new user has completed the registration form on
        the client application"""


        #Preparing the insertion query
        query = "INSERT INTO user (UserName,Email,Name,Surname,Password,PublicKey) VALUES ('%s','%s','%s','%s','%s','%s') " \
        % (user,email,name,surname,password,str(key))
        try:
            #Executing the query
            self.cursor.execute(query)
            #Commit the changes to the databes
            self.db.commit()
            return 0
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the user insertion query")
            return -1

    #This method is used to store a message in the database and is invoked when the receiver of that message is offline,
    #in order to send it when the last one will back online


    def insert_message(self,sender,receiver,message,time):
        #Preparing the insertion query
        query = "INSERT INTO message(Sender,Receiver,Text,Time) VALUES ('%s','%s','%s','%s') " \
        % (sender,receiver,message,time)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Commit the changes to the databes
            self.db.commit()
            return 0
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the message insertion query")
            return -1
    def getMessageByReceiver(self,receiver):
        query = "SELECT Sender,Text,Time FROM message WHERE Receiver = '%s'" %(receiver)
        msg = []
        try:
            #Executing the query
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                #print(str(row[-1]))
                msg_t = [str(i) for i in row]
                #print(msg_t)
                msg.append('/^'.join(msg_t))
            msg = str('^/'.join(msg))
            print(msg)
            return msg
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the message insertion query")
            return -1

    def userIsPresent(self,_user,_password):
        query = "SELECT * from user where UserName = '%s' AND Password = '%s' " % (_user,_password)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Obtaining the result as a list
            results = self.cursor.fetchall()
            return len(results) == 1
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the select query")
            return -1
    def userIsRegistered(self,_user):
        query = "SELECT * from user where UserName = '%s' " % (_user)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Obtaining the result as a list
            results = self.cursor.fetchall()
            return len(results) == 1
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the select query")
            return -1

    #If a user want to unscribe to our platform he can do it and this method is used to remove all his information from
    #the database

    def remove_user(self,user):
        query = "DELETE from user WHERE UserName = '%s'" % (user)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Commit the changes to the databes
            self.db.commit()
            return 0
        except:
            #rollback the previous operations
            self.db.rollback()
            print ("Error in the user delete query")
            return -1

    #This method is invkoed when a user back online and there are several waiting message with him as receiver.

    def remove_waiting_messages_by_receiver(self,receiver):
        query = "DELETE from message WHERE Receiver = %s" % (receiver)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Commit the changes to the databes
            self.db.commit()
            return 0
        except:
            #rollback the previous operations
            self.db.rollback()
            print ("Error in the message delete query")
            return -1

    def remove_waiting_messages_by_sender(self,sender):
        query = "DELETE from message WHERE Sender = %s" % (sender)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Commit the changes to the databes
            self.db.commit()
            return 0
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the message delete query")
            return -1
    def remove_waiting_messages_by_id(self,index):
        query = "DELETE from message WHERE Index = %s" % (index)
        try:
            #Executing the query
            self.cursor.execute(query)
            #Commit the changes to the databes
            self.db.commit()
            return 0
        except:
            #rollback to the previous operations
            self.db.rollback()
            print ("Error in the message delete query")
            return -1

    #At the end of the execetion the server close the connection with the database invoking this method

    def close_connection(self):
        self.db.close()
