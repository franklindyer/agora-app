class AgoraFilter:
    def __init__(self, nextFilter):
        self.next = nextFilter

    def createAccount(self, emailAddress, username, hpassword, acceptable):
        raise NotImplementedError
    def confirmCreate(self, uid):
        raise NotImplementedError

    def login(self, uid):
        raise NotImplementedError
    def logout(self, sessionToken):
        raise NotImplementedError

    def deleteAccount(self, uid, email):
        raise NotImplementedError
    def confirmDelete(self, uid):
        raise NotImplementedError

    def recoverAccount(self, emailAddress, acceptable):
        raise NotImplementedError
    def backupRecover(self, uid, emailAddress):
        raise NotImplementedError
    def confirmRecover(self, uid, hpassword):
        raise NotImplementedError

    def changeStatus(self, uid, newStatus):
        raise NotImplementedError
    def changePicture(self, uid, imageId):
        raise NotImplementedError
    def changeEmail(self, uid, emailAddress, acceptable):
        raise NotImplementedError
    def changeUsername(self, uid, username):
        raise NotImplementedError

    def writePost(self, uid, title, content):
        raise NotImplementedError
    def deletePost(self, pid):
        raise NotImplementedError
    def uploadImage(self, uid, title, imgData):
        raise NotImplementedError
    def deleteImage(self, imageId):
        raise NotImplementedError

    def friendRequest(self, uid1, uid2):
        raise NotImplementedError

    def comment(self, uid, pid, content):
        raise NotImplementedError

    def bugReport(self, uid, content):
        raise NotImplementedError

    def adminSuspend(self, uid):
        raise NotImplementedError
    def adminUnsuspend(self, uid):
        raise NotImplementedError
    def adminDelete(self, uid):
        raise NotImplementedError
