from Server import Server
from Database.Database import Database
s = Server(6000)
try:
    s.start()
except KeyboardInterrupt:
    s.close()
