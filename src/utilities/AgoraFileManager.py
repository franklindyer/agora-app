import os
from agora_errors import *

class AgoraFileManager:
    def __init__(self, postdir, imgdir):
        self.postdir = postdir
        self.imgdir = imgdir

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

    def relativizeImagePath(self, filename):
        return os.path.join(self.imgdir, filename)
