from Server import Server
s = Server(6000)
try:
    s.start()
except KeyboardInterrupt:
    s.close()
