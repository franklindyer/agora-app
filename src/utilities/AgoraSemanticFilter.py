from AgoraFilter import *
from agora_errors import *
from limits import *
import requests

class AgoraSemanticFilter(AgoraFilter):
    def setDBManager(self, db):
        self.db = db

    def setReCaptchaKey(self, key):
        self.reCaptchaServerKey = key


    def doLogin(self, sessionToken):
        uid = self.db.tokenExists(sessionToken, "session")
        if uid is None:
            raise AgoraEInvalidToken
        if self.db.isUserSuspended(uid):
            raise AgoraENotAuthorized
        if self.db.getTokenAgeSeconds(sessionToken) > SESSION_MAX_DURATION_SECONDS:
            self.db.expireToken(sessionToken)   # Here I am breaking my unspoken rule that AgoraSemanticFilter not write to the DB
            raise AgoraENotLoggedIn
        return uid

    def applyTimeLimit(self, uid):
        if self.db.getUserLastAction(uid) < USER_ACTION_TIMEOUT_SECONDS:
            raise AgoraETooSoon
        else:
            self.db.setUserLastAction(uid)      # Here I am breaking that unspoken rule again!

    def verifyCaptcha(self, userresp):
        reCaptchaUrl = "https://www.google.com/recaptcha/api/siteverify"
        resp = requests.post(reCaptchaUrl, data={"secret": self.reCaptchaServerKey, "response": userresp})
        if resp.json()["score"] < RECAPTCHA_THRESHHOLD:
            raise AgoraEAreYouHuman



    def createAccount(self, emailAddress, username, hpassword, captcha):
        self.verifyCaptcha(captcha)
        uid = self.db.emailExists(emailAddress)     # We don't raise an error when uid is None, in order to avoid disclosing emails
        old_uid =  self.db.usernameExists(username)
        if (not old_uid is None) and self.db.isUserConfirmed(old_uid):
            raise AgoraEInvalidUsername
        existing_user_confirmed = (uid is None) or (not self.db.isUserConfirmed(uid))   # Unconfirmed accounts get clobbered by new account creation attempts
        return self.next.createAccount(emailAddress, username, hpassword, existing_user_confirmed)

    def confirmCreate(self, creationToken):
        uid = self.db.tokenExists(creationToken, "creation")
        if uid is None:
            raise AgoraEInvalidToken
        return self.next.confirmCreate(uid, creationToken)



    def login(self, username, hpassword):
        uid = self.db.passwordCorrect(username, hpassword)
        if uid is None:
            raise AgoraEIncorrectCreds
        if self.db.isUserSuspended(uid):
            raise AgoraENotAuthorized
        if not self.db.isUserConfirmed(uid):
            raise AgoraENotAuthorized
        return self.next.login(uid)

    def logout(self, sessionToken):
        if not self.db.tokenExists(sessionToken, "session"):
            raise AgoraEInvalidToken
        return self.next.logout(sessionToken)



    def deleteAccount(self, sessionToken, hpassword):
        uid = self.db.tokenExists(sessionToken, "session")
        if uid is None:
            raise AgoraEInvalidToken
        dat = self.db.getPrivateUser(uid)
        username = dat['username']
        email = dat['email']
        if not self.db.passwordCorrect(username, hpassword):
            raise AgoraEIncorrectCreds
        return self.next.deleteAccount(uid, email)

    def confirmDelete(self, deletionToken):
        uid = self.db.tokenExists(deletionToken, "deletion")
        if uid is None:
            raise AgoraEInvalidToken
        return self.next.confirmDelete(uid)


    def recoverAccount(self, emailAddress):
        uid = self.db.emailExists(emailAddress)     # We don't raise an error when uid is None, in order to avoid disclosing emails
        return self.next.recoverAccount(emailAddress, not (uid is None))

    def backupRecover(self, hrecovery, emailAddress):
        uid = self.db.getRecovery(hrecovery)
        if uid is None:
            raise AgoraEInvalidToken
        return self.next.backupRecover(uid, emailAddress)

    def confirmRecover(self, recoveryToken, hpassword):
        uid = self.db.tokenExists(recoveryToken, "recovery")
        if uid is None:
            raise AgoraEInvalidToken
        return self.next.confirmRecover(uid, hpassword)



    def getUser(self, uid):
        if self.db.userExists(uid) is None:
            raise AgoraENoSuchUser
        return self.db.getPublicUser(uid)

    def getPost(self, pid):
        if self.db.postExists(pid) is None:
            raise AgoraENoSuchPost
        return self.db.getPostInfo(pid)
    
    def getImage(self, imageId):
        loc = self.db.imgExists(imageId)
        if loc is None:
            raise AgoraENoSuchImage
        return loc
    
    def searchUsers(self, query):
        return self.db.searchUser(query)
    
    def searchPosts(self, query):
        return self.db.searchPost(query)



    def getMyUser(self, sessionToken, concise=False):
        uid = self.doLogin(sessionToken)
        return self.db.getPrivateUser(uid, concise=concise)



    def changeStatus(self, sessionToken, newStatus):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        return self.next.changeStatus(uid, newStatus)

    def changePicture(self, sessionToken, imageId):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        return self.next.changePicture(uid, imageId)
    
    def changeEmail(self, sessionToken, emailAddress):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        otherOwner = self.db.emailExists(emailAddress)  # We don't raise an error when uid is None, in order to avoid disclosing emails
        return self.next.changeEmail(uid, emailAddress, otherOwner is None)
   
    def confirmEmail(self, emailToken):
        uid = self.db.tokenExists(emailToken, "email")
        if uid is None:
            raise AgoraEInvalidToken
        return self.next.confirmEmail(uid, emailToken)

    def changeUsername(self, sessionToken, username):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        if not self.db.usernameExists(username) is None:
            raise AgoraEInvalidUsername
        return self.next.changeUsername(uid, username)



    def writePost(self, sessionToken, title, content):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        return self.next.writePost(uid, title, content)

    def editPost(self, sessionToken, pid, title, content):
        uid = self.doLogin(sessionToken)
        if self.db.postExists(pid) is None:
            raise AgoraENoSuchPost
        pinfo = self.db.getPostInfo(pid)
        if pinfo['owner'] != uid:
            raise AgoraENotAuthorized
        return self.next.editPost(pid, title, content)
           
 
    def deletePost(self, sessionToken, pid):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        if self.db.postExists(pid) is None:
            raise AgoraENoSuchPost
        pinfo = self.db.getPostInfo(pid)
        if pinfo['owner'] != uid:
            raise AgoraENotAuthorized
        return self.next.deletePost(pid)
    
    def uploadImage(self, sessionToken, title, extension, imgData):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        numImages = self.db.getNumImages(uid)
        if numImages > USER_MAX_IMAGES:
            raise AgoraEBadImage
        return self.next.uploadImage(uid, title, extension, imgData)
    
    def deleteImage(self, sessionToken, imageId):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        if self.db.imgExists(imageId) is None:
            raise AgoraENoSuchImage
        imgowner = self.db.getImageOwner(imageId)
        if imgowner != uid:
            raise AgoraENotAuthorized
        return self.next.deleteImage(imageId)
    
    def listImages(self, sessionToken):
        uid = self.doLogin(sessionToken)
        info = self.db.getPrivateUser(uid)
        return info["images"]



    def friendRequest(self, sessionToken, uid2):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        if self.db.userExists(uid2) is None:
            raise AgoraENoSuchUser
        return self.next.friendRequest(uid, uid2)
    
    def viewFriendReqs(self, sessionToken):
        uid = self.doLogin(sessionToken)
        info = self.db.getPrivateUser(uid)
        return info["foryou"]
    
    def acceptFriendReq(self, sessionToken, uid2):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        if self.db.userExists(uid2) is None:
            raise AgoraENoSuchUser
        return self.next.friendRequest(uid, uid2)



    def comment(self, sessionToken, pid, content):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        if self.db.postExists(pid) is None:
            raise AgoraENoSuchPost
        return self.next.comment(uid, pid, content)



    def bugReport(self, sessionToken, content):
        uid = self.doLogin(sessionToken)
        self.applyTimeLimit(uid)
        return self.bugReport(uid, content)



    def adminGetUser(self, sessionToken, uid):
        my_uid = self.doLogin(sessionToken)
        if not self.db.isUserAdmin(my_uid):
            raise AgoraENotAuthorized
        if self.db.userExists(uid) is None:
            raise AgoraENoSuchUser
        return self.db.getPrivateUser(uid)
    

    def adminSuspend(self, sessionToken, uid):
        my_uid = self.doLogin(sessionToken)
        if not self.db.isUserAdmin(my_uid):
            raise AgoraENotAuthorized
        if self.db.userExists(uid) is None:
            raise AgoraENoSuchUser
        if self.db.isUserAdmin(uid):
            raise AgoraENotAuthorized       # Admins cannot suspend other admins
        return self.next.adminSuspend(uid)
    

    def adminUnsuspend(self, sessionToken, uid):
        my_uid = self.doLogin(sessionToken)
        if not self.db.isUserAdmin(my_uid):
            raise AgoraENotAuthorized
        if self.db.userExists(uid) is None:
            raise AgoraENoSuchUser
        if self.db.isUserAdmin(uid):
            raise AgoraENotAuthorized       # Admins cannot suspend other admins
        return self.next.adminUnsuspend(uid)


    def adminDelete(self, sessionToken, uid, hpassword):
        my_uid = self.doLogin(sessionToken)
        my_user = self.db.getPublicUser(uid)["username"]
        if not self.db.isUserAdmin(my_uid):
            raise AgoraENotAuthorized
        if self.db.userExists(uid) is None:
            raise AgoraENoSuchUser
        if self.db.passwordCorrect(my_user, hpassword) is None:
            raise AgoraEIncorrectCreds
        if self.db.isUserAdmin(uid):
            raise AgoraENotAuthorized       # Admins cannot delete other admins
        return self.next.adminDelete(uid)
