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

    def createAccount(self, emailAddress, username, hpassword, acceptable):
        old_uid = self.db.emailExists(emailAddress)
        if not old_uid is None:
            self.db.deleteUser(old_uid)     # Delete any unconfirmed accounts with this address
        if acceptable:
            recovery = self.generateToken("recovery")
            hrecovery = hashlib.sha256(recovery.encode()).hexdigest()
            uid = self.db.createUser(emailAddress, username, hpassword, hrecovery)
            confirm = self.generateToken("creation")
            confirmUrl = f'{self.host}/join/{confirm}'
            self.eml.confirmAccountEmail(emailAddress, confirmUrl)
            self.db.createToken(uid, confirm, "creation")
    
    def confirmCreate(self, uid, creationToken):
        self.db.expireToken(creationToken)
        self.db.verifyUser(uid)

    def login(self, uid):
        session = self.generateToken("session")
        self.db.createToken(uid, session, "session")
        return session

    def logout(self, sessionToken):
        self.db.expireToken(sessionToken)

    def deleteAccount(self, uid, emailAddress):
        confirm = self.generateToken("deletion")
        self.db.createToken(uid, confirm, "deletion")
        confirmUrl = f'{self.host}/leave/{confirm}'
        self.eml.deleteAccountEmail(emailAddress, confirmUrl)

    def confirmDelete(self, uid):
        self.db.deleteUser(uid)

    def recoverAccount(self, emailAddress, acceptable):
        raise NotImplementedError
    
    def confirmRecover(self, uid, hpassword):
        raise NotImplementedError

    def backupRecover(self, uid, emailAddress):
        self.changeEmail(uid, emailAddress, True)



    def changeStatus(self, uid, newStatus):
        self.db.setStatus(uid, newStatus)

    def changePicture(self, uid, imageId):
        raise NotImplementedError
    
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
        self.eml.newRecoveryToken(newEmail, recovery)
        self.db.setRecovery(uid, hrecovery)

    def changeUsername(self, uid, username):
        self.db.setUsername(uid, username)



    def writePost(self, uid, title, content):
        filename = f"post{self.generateToken('postid')}.md"
        self.db.insertPost(uid, title, filename)
        self.fm.writePost(filename, content)

    def deletePost(self, pid):
        self.db.deletePost(pid)
    
    def uploadImage(self, uid, title, imgData):
        raise NotImplementedError
    
    def deleteImage(self, imageId):
        raise NotImplementedError



    def friendRequest(self, uid1, uid2):
        raise NotImplementedError

    def comment(self, uid, pid, content):
        self.db.insertComment(uid, pid, content)

    def bugReport(self, uid, content):
        raise NotImplementedError



    def adminSuspend(self, uid):
        self.db.suspendUser(uid)
    
    def adminUnsuspend(self, uid):
        self.db.unsuspendUser(uid)
    
    def adminDelete(self, uid):
        self.db.deleteUser(uid)
