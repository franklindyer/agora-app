class AgoraFilter:
    def createAccount(emailAddress, username, password):
        raise NotImplementedError
    def confirmCreate(creationToken):
        raise NotImplementedError

    def login(username, password):
        raise NotImplementedError
    def logout(sessionToken):
        raise NotImplementedError

    def deleteAccount(sessionToken, password):
        raise NotImplementedError
    def confirmDelete(deletionToken):
        raise NotImplementedError

    def recoverAccount(emailAddress):
        raise NotImplementedError
    def backupRecover(backupCode, emailAddress):
        raise NotImplementedError
    def confirmRecover(recoveryToken, password):
        raise NotImplementedError

    def getUser(uid):
        raise NotImplementedError
    def getPost(pid):
        raise NotImplementedError
    def getImage(imageId):
        raise NotImplementedError
    def searchUsers(query):
        raise NotImplementedError
    def searchPosts(query):
        raise NotImplementedError

    def getMyUser(sessionToken):
        raise NotImplementedError

    def changeStatus(sessionToken, newStatus):
        raise NotImplementedError
    def changePicture(sessionToken, imageId):
        raise NotImplementedError
    def changeEmail(sessionToken, emailAddress):
        raise NotImplementedError
    def changeUsername(sessionToken, username):
        raise NotImplementedError

    def writePost(sessionToken, title, content):
        raise NotImplementedError
    def deletePost(sessionToken, pid):
        raise NotImplementedError
    def uploadImage(sessionToken, title, imgData):
        raise NotImplementedError
    def deleteImage(sessionToken, imageId):
        raise NotImplementedError
    def listImages(sessionToken):
        raise NotImplementedError

    def friendRequest(sessionToken, uid):
        raise NotImplementedError
    def viewFriendReqs(sessionToken):
        raise NotImplementedError
    def acceptFriendReq(sessionToken, uid):
        raise NotImplementedError

    def comment(sessionToken, pid):
        raise NotImplementedError

    def bugReport(sessionToken, content):
        raise NotImplementedError

    def adminGetUser(sessionToken, uid):
        raise NotImplementedError
    def adminSuspend(sessionToken, uid):
        raise NotImplementedError
    def adminUnsuspend(sessionToken, uid):
        raise NotImplementedError
    def adminDelete(sessionToken, uid, password):
        raise NotImplementedError
