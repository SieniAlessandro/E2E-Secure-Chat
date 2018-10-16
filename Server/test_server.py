from Server import Server
from Database.Database import Database
s = Server(6000)
db = Database('localhost',3306,'root','rootroot','messaggistica_mps')
"""
try:
    s.start()
except KeyboardInterrupt:
    s.close()
"""
db.getMessageByReceiver("a")
