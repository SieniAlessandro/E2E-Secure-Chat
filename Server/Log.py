import threading
import datetime
class Log:
    def __init__(self,enableLog,path):
        self.enableLog = enableLog
        self.lock = threading.Lock()
        self.file = open(path,"w")
    def log(self,_log):
        with self.lock:
            if self.enableLog:
                time = str(datetime.datetime.now()).split('.')[0]
                text = str(time) + "\t"+str(_log)+"\n"
                self.file.write(text)
                self.file.flush()
    def closeFile(self):
        self.file.close()
