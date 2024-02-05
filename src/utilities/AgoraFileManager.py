import os

class AgoraFileManager:
    def __init__(self, folder):
        self.homedir = folder

    def writePost(self, filename, content):
        path = os.path.join(self.homedir, filename)
        with open(path, 'w+') as f:
            f.write(content)
