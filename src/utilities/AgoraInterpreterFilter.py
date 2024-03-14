import hashlib
import random, string
from limits import *

class AgoraInterpreterFilter:
    def __init__(self, nextFilter):
        self.next = nextFilter

    def setDBManager(self, db):
        self.db = db

    def setEmailer(self, eml):
        self.eml = eml

    def setHost(self, host):
        self.host = host

    def setFileManager(self, fm):
        self.fm = fm

    def generateToken(self, ttype):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(TOKEN_LENGTHS[ttype]))

    def replenishCSRF(self, uid):
        newCSRF = self.generateToken('csrf')
        self.db.replaceCSRF(uid, newCSRF)

    def createAccount(self, emailAddress, username, hpassword, acceptable):
        old_uid = self.db.emailExists(emailAddress)
        if not old_uid is None:
            self.db.deleteUser(old_uid)     # Delete any unconfirmed accounts with this address
        if acceptable:
            recovery = self.generateToken("backup")
            hrecovery = hashlib.sha256(recovery.encode()).hexdigest()
            uid = self.db.createUser(emailAddress, username, hpassword, hrecovery, "0"*IMG_RANDOM_ID_LENGTH)
            confirm = self.generateToken("creation")
            confirmUrl = f'{self.host}/join/{confirm}'
            self.eml.confirmAccountEmail(emailAddress, confirmUrl)
            self.db.createToken(uid, confirm, "creation", data=recovery)
    
    def confirmCreate(self, uid, creationToken):
        recovery = self.db.tokenData(creationToken)
        self.db.expireToken(creationToken)
        self.db.verifyUser(uid)
        return recovery

    def login(self, uid):
        session = self.generateToken("session")
        self.db.createToken(uid, session, "session")
        self.replenishCSRF(uid)
        return session

    def logout(self, uid):
        self.db.expireAllSessions(uid)

    def deleteAccount(self, uid, emailAddress):
        confirm = self.generateToken("deletion")
        self.db.createToken(uid, confirm, "deletion")
        confirmUrl = f'{self.host}/leave/{confirm}'
        self.eml.deleteAccountEmail(emailAddress, confirmUrl)

    def confirmDelete(self, uid):
        self.db.deleteUser(uid)



    def recoverAccount(self, uid, emailAddress, acceptable):
        if not acceptable:
            return
        recoveryToken = self.generateToken("recovery")
        self.db.createToken(uid, recoveryToken, "recovery")
        self.eml.recoverAccountEmail(emailAddress, f"{self.host}/changepass/{recoveryToken}")
 
    def confirmRecover(self, uid, recoveryToken, hpassword):
        self.db.expireToken(recoveryToken)
        self.db.setPassword(uid, hpassword)

    def backupRecover(self, uid, hbackup, emailAddress, acceptable=True):
        self.changeEmail(uid, emailAddress, acceptable)



    def changeStatus(self, uid, newStatus):
        self.db.setStatus(uid, newStatus)

    def changePicture(self, uid, imageId):
        self.db.setPicture(uid, imageId)
    
    def changeEmail(self, uid, emailAddress, acceptable):
        emailToken = self.generateToken("email")
        self.db.createToken(uid, emailToken, "email", data=emailAddress)
        confirmUrl = f'{self.host}/confirmemail/{emailToken}'
        self.eml.changeAccountEmail(emailAddress, confirmUrl)
   
    def confirmEmail(self, uid, emailToken):
        newEmail = self.db.tokenData(emailToken)
        self.db.expireToken(emailToken)
        self.db.setEmail(uid, newEmail)
        recovery = self.generateToken("recovery")
        hrecovery = hashlib.sha256(recovery.encode()).hexdigest()
        self.db.setBackup(uid, hrecovery)
        return recovery

    def changeUsername(self, uid, username):
        self.db.setUsername(uid, username)



    def writePost(self, uid, title, content):
        filename = f"post{self.generateToken('postid')}.md"
        pid = self.db.insertPost(uid, title, filename)
        self.fm.writePost(filename, content)
        return pid

    def editPost(self, pid, title, content):
        filename = self.db.getPostInfo(pid)["filename"]
        self.db.updatePost(pid, title)
        self.fm.editPost(filename, content)

    def deletePost(self, pid):
        filename = self.db.getPostInfo(pid)["filename"]
        self.db.deletePost(pid)
        self.fm.deletePost(filename)
    
    def uploadImage(self, uid, title, extension, imgData):
        accessid = self.generateToken('imgid')
        filename = f"img{accessid}.{extension}"
        self.db.insertImage(uid, title, filename, accessid)
        self.fm.saveImage(filename, imgData)
        return accessid

    def deleteImage(self, imageId):
        filename = self.db.imgExists(imageId)
        self.db.deleteImage(imageId)
        self.fm.deleteImage(filename) 



    def friendRequest(self, uid1, uid2):
        self.db.insertFriendReq(uid1, uid2)

    def unfriend(self, uid1, uid2):
        self.db.deleteFriendReq(uid1, uid2)

    def comment(self, uid, pid, content):
        self.db.insertComment(uid, pid, content)

    def deleteComment(self, cid):
        self.replenishCSRF(uid)
        return self.db.deleteComment(cid)
    
    def like(self, uid, pid):
        self.db.likePost(uid, pid)
    
    def unlike(self, uid, pid):
        self.db.unlikePost(uid, pid)
    
    def dislike(self, uid, pid):
        self.db.dislikePost(uid, pid)

    def bugReport(self, uid, content):
        rid = self.db.createBugReport(uid)
        self.eml.bugReport(rid, uid, content)
        return rid



    def adminSuspend(self, uid):
        self.db.suspendUser(uid)
    
    def adminUnsuspend(self, uid):
        self.db.unsuspendUser(uid)
    
    def adminDelete(self, uid):
        self.db.deleteUser(uid)
