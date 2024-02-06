import os

class AgoraFileManager:
    def __init__(self, postdir, imgdir):
        self.postdir = postdir
        self.imgdir = imgdir

    def writePost(self, filename, content):
        path = os.path.join(self.homedir, filename)
        with open(path, 'w+') as f:
            f.write(content)

    def saveImage(self, filename, file):
        path = os.path.join(self.imgdir, filename)
        file.save(path)

    def relativizeImagePath(self, filename):
        return os.path.join(self.imgdir, filename)
