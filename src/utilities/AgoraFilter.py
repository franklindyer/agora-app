class AgoraFilter:
    def __init__(self, nextFilter):
        self.next = nextFilter

    def createAccount(self, emailAddress, username, password):
        raise NotImplementedError
    def confirmCreate(self, creationToken):
        raise NotImplementedError

    def login(self, username, password):
        raise NotImplementedError
    def logout(self, sessionToken):
        raise NotImplementedError

    def deleteAccount(self, sessionToken, password):
        raise NotImplementedError
    def confirmDelete(self, deletionToken):
        raise NotImplementedError

    def recoverAccount(self, emailAddress):
        raise NotImplementedError
    def backupRecover(self, backupCode, emailAddress):
        raise NotImplementedError
    def confirmRecover(self, recoveryToken, password):
        raise NotImplementedError

    def getUser(self, uid):
        raise NotImplementedError
    def getPost(self, pid):
        raise NotImplementedError
    def getImage(self, imageId):
        raise NotImplementedError
    def searchUsers(self, query):
        raise NotImplementedError
    def searchPosts(self, query):
        raise NotImplementedError

    def getMyUser(self, sessionToken):
        raise NotImplementedError

    def changeStatus(self, sessionToken, newStatus):
        raise NotImplementedError
    def changePicture(self, sessionToken, imageId):
        raise NotImplementedError
    def changeEmail(self, sessionToken, emailAddress):
        raise NotImplementedError
    def changeUsername(self, sessionToken, username):
        raise NotImplementedError

    def writePost(self, sessionToken, title, content):
        raise NotImplementedError
    def deletePost(self, sessionToken, pid):
        raise NotImplementedError
    def uploadImage(self, sessionToken, title, imgData):
        raise NotImplementedError
    def deleteImage(self, sessionToken, imageId):
        raise NotImplementedError
    def listImages(self, sessionToken):
        raise NotImplementedError

    def friendRequest(self, sessionToken, uid):
        raise NotImplementedError
    def viewFriendReqs(self, sessionToken):
        raise NotImplementedError
    def acceptFriendReq(self, sessionToken, uid):
        raise NotImplementedError

    def comment(self, sessionToken, pid):
        raise NotImplementedError

    def bugReport(self, sessionToken, content):
        raise NotImplementedError

    def adminGetUser(self, sessionToken, uid):
        raise NotImplementedError
    def adminSuspend(self, sessionToken, uid):
        raise NotImplementedError
    def adminUnsuspend(self, sessionToken, uid):
        raise NotImplementedError
    def adminDelete(self, sessionToken, uid, password):
        raise NotImplementedError
