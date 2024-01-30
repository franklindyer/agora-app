class AgoraSyntacticFilter:

    def validateEmail(self, emailAddress):
        if email.utils.parseaddr(emailAddress) == ('', ''):
            raise AgoraEInvalidEmail
    
    def isLengthBetween(self, str, lower, upper):
        length = len(str)
        return ((length > upper) or (length < lower))

    def validateUsername(self, username):
        if not self.isLengthBetween(username, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH):
            raise AgoraEInvalidUsername

    def validatePassword(self, password):
        if not self.isLengthBetween(password, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH):
            raise AgoraEInvalidPassword
        return hashlib.new('sha256').update(password.encode()).hexdigest()

    TOKEN_LENGTHS = {
        "creation": ACCOUNT_CREATION_TOKEN_LENGTH,
        "deletion": ACCOUNT_DELETION_TOKEN_LENGTH,
        "recovery": ACCOUNT_RECOVERY_TOKEN_LENGTH,
        "backup": ACCOUNT_BACKUP_KEY_LENGTH,
        "session": SESSION_TOKEN_LENGTH
    }

    def validateToken(self, token, tokenType):
        expectLength = self.TOKEN_LENGTHS[tokenType]
        if len(token) != expectLength:
            raise AgoraEInvalidToken
        if not token.isalnum():
            raise AgoraEInvalidToken

    def validateStatus(self, status):
        if not self.isLengthBetween(status, STATUS_MIN_LENGTH, STATUS_MAX_LENGTH):
            raise AgoraEInvalidStatus

    def validatePost(self, content):
        if not self.isLengthBetween(content, 0, POST_MAX_LENGTH):
            raise AgoraEInvalidPost

    def validatePostTitle(self, title):
        if not self.isLengthBetween(content, POST_TITLE_MIN_LENGTH, POST_TITLE_MAX_LENGTH):
            raise AgoraEInvalidTitle

    def validateImageTitle(self, title):
        if not self.isLengthBetween(content, IMG_TITLE_MIN_LENGTH, IMG_TITLE_MAX_LENGTH):
            raise AgoraEInvalidTitle

    def validateImage(self, imgData):
        raise NotImplementedError

    def validateComment(self, comment):
        if not self.isLengthBetween(content, COMMENT_MIN_LENGTH, COMMENT_MAX_LENGTH):
            raise AgoraEInvalidComment

    def validateReport(self, content):
        if not self.isLengthBetween(content, BUG_REPORT_MIN_LENGTH, BUG_REPORT_MAX_LENGTH):
            raise AgoraEInvalidReport

    def validateQuery(self, content):
        if not self.isLengthBetween(content, 0, QUERY_MAX_LENGTH):
            raise AgoraEInvalidQuery

    def isValidId(self, str):
        return str.isdigit()



    def createAccount(self, emailAddress, username, password):
        self.validateEmail(emailAddress)
        self.validateUsername(username)
        hpassword = self.validatePassword(password)
        return self.next.createAccount(emailAddress, username, hpassword)

    def confirmCreate(self, creationToken):
        self.validateToken(creationToken, "creation")
        return self.next.confirmCreate(creationToken)



    def login(self, username, password):
        self.validateUsername(username)
        hpassword = self.validatePassword(password)
        return self.next.login(username, hpassword)

    def logout(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.logout(sessionToken)



    def deleteAccount(self, sessionToken, password):
        self.validateToken(sessionToken, "session")
        hpassword = self.validatePassword(password)
        return self.next.deleteAccount(sessionToken, password)

    def confirmDelete(self, deletionToken):
        self.validateToken(sessionToken, "deletion")
        return self.next.confirmDelete(deletionToken)



    def recoverAccount(self, emailAddress):
        self.validateEmail(emailAddress)
        return self.next.recoverAccount(emailAddress)

    def backupRecover(self, backupCode, emailAddress):
        self.validateToken(backupCode, "backup")
        self.validateEmail(emailAddress)
        return self.next.backupRecover(backupCode, emailAddress)

    def confirmRecover(self, recoveryToken, password):
        self.validateToken(recoveryToken, "recovery")
        hpassword = self.validatePassword(password)
        return self.next.confirmRecover(recoveryToken, hpassword)



    def getUser(self, uid):
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.getUser(int(uid))
    
    def getPost(self, pid):
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.getPost(int(pid))
    
    def getImage(self, imageId):
        if not self.isValidId(imageId):
            raise AgoraENoSuchImage
        return self.next.getImage(int(imageId))
    
    def searchUsers(self, query):
        self.validateQuery(query)
        return self.next.searchUsers(query)
    
    def searchPosts(self, query):
        self.validateQuery(query)
        return self.next.searchPosts(query)



    def getMyUser(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.getMyUser(sessionToken)



    def changeStatus(self, sessionToken, newStatus):
        self.validateToken(sessionToken, "session")
        self.validateStatus(newStatus)
        return self.next.changeStatus(sessionToken, newStatus)
    
    def changePicture(self, sessionToken, imageId):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(imageId):
            raise ENoSuchImage
        return self.next.changePicture(sessionToken, int(imageId))
    
    def changeEmail(self, sessionToken, emailAddress):
        self.validateToken(sessionToken, "session")
        self.validateEmail(emailAddress)
        return self.next.changeEmail(sessionToken, emailAddress)

    def changeUsername(self, sessionToken, username):
        self.validateToken(sessionToken, "session")
        self.validateUsername(username)
        return self.next.changeUsername(sessionToken, username)

    def writePost(self, sessionToken, title, content):
        self.validateToken(sessionToken, "session")
        self.validatePostTitle(title)
        self.validatePost(content)
        return self.next.writePost(sessionToken, title, content)
    
    def deletePost(self, sessionToken, pid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.deletePost(sessionToken, int(pid))
    
    def uploadImage(self, sessionToken, title, imgData):
        self.validateToken(sessionToken, "session")
        self.validateImageTitle(title)
        self.validateImage(imgData)
        return self.next.uploadImage(sessionToken, title, imgData)
    
    def deleteImage(self, sessionToken, imageId):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(imageId):
            raise AgoraENoSuchImage
        return self.next.deleteImage(sessionToken, int(imageId))

    def listImages(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.listImages(sessionToken)



    def friendRequest(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.friendRequest(sessionToken, int(uid))

    def viewFriendReqs(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.viewFriendReqs(sessionToken)
    
    def acceptFriendReq(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.acceptFriendReq(sessionToken, int(uid))



    def comment(self, sessionToken, pid, content):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        self.validateComment(content)
        return self.next.comment(sessionToken, int(pid), content)

    def bugReport(self, sessionToken, content):
        self.validateToken(sessionToken, "session")
        self.validateReport(content)
        return self.next.bugReport(sessionToken, content)



    def adminGetUser(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid)
            raise AgoraENoSuchUser
        return self.next.adminGetUser(sessionToken, int(uid))

    def adminSuspend(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid)
            raise AgoraENoSuchUser
        return self.next.adminSuspendUser(sessionToken, int(uid))

    def adminUnsuspend(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid)
            raise AgoraENoSuchUser
        return self.next.adminUnsuspendUser(sessionToken, int(uid))
    
    def adminDelete(self, sessionToken, uid, password):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid)
            raise AgoraENoSuchUser
        hpassword = self.validatePassword(password)
        return self.next.adminDelete(sessionToken, int(uid), hpassword)
