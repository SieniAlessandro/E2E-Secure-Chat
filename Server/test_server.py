from Server import Server
from Database.Database import Database
s = Server()
try:
    s.start()
except KeyboardInterrupt:
    s.close()
