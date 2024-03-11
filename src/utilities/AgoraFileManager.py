from multiprocessing.pool import ThreadPool
from datetime import datetime
from agora_errors import *
from multiprocessing.pool import ThreadPool
from datetime import datetime
import os
from agora_errors import *

class AgoraFileManager:
    def __init__(self, postdir, imgdir, logdir):
        self.postdir = postdir
        self.imgdir = imgdir
        self.logdir = logdir
        self.logPool = ThreadPool(processes=1)

    def getPost(self, filename):
        path = os.path.join(self.postdir, filename)
        if os.path.isfile(path):
            return open(path, 'r').read()
        else:
            raise AgoraENoSuchPost

    def getPost(self, filename):
        path = os.path.join(self.postdir, filename)
        if os.path.isfile(path):
            return open(path, 'r').read()
        else:
            raise AgoraENoSuchPost

    def writePost(self, filename, content):
        path = os.path.join(self.postdir, filename)
        with open(path, 'w+') as f:
            f.write(content)

    def editPost(self, filename, content):
        path = os.path.join(self.postdir, filename)
        with open(path, 'w') as f:
            f.write(content)

    def saveImage(self, filename, file):
        path = os.path.join(self.imgdir, filename)
        file.save(path)

    def deleteImage(self, filename):
        os.remove(os.path.join(self.imgdir, filename))

    def deletePost(self, filename):
        os.remove(os.path.join(self.postdir, filename))

    def relativizeImagePath(self, filename):
        return os.path.join(self.imgdir, filename)

    def poolLog(self, msg):
        path = os.path.join(self.logdir, f"{datetime.today().strftime('%Y-%m-%d')}.log")
        with open(path, 'a+') as f:
            f.write(f"{datetime.now().strftime('%I:%M%p')} | {msg}\n")

    def log(self, msg):
        return self.logPool.apply(self.poolLog, (msg,))

    def logif(self, cond, msg):
        if cond:
            self.log(msg)

