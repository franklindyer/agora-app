import os, sqlite3
from multiprocessing.pool import ThreadPool

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class AgoraDatabaseManager:
    def __init__(self, dbname):
        self.dbname = dbname
        self.readPool = ThreadPool(processes=10)
        self.writePool = ThreadPool(processes=1)
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
        self.conn.row_factory = dict_factory

    def commit(self):
        self.conn.commit()

    def cur(self):
        cur = self.conn.cursor()
        cur.row_factory = dict_factory
        return cur

    def pool_query(self, query, args=()):
        cur = self.cur().execute(query, args)
        res = [x for x in cur.fetchall()]
        cur.close()
        return (res if len(res) > 0 else None)

    def pool_execute(self, query, args=()):
        cur = self.cur().execute(query, args)
        cur.close()
        self.commit()

    def query(self, query, args=()):
        return self.readPool.apply(self.pool_query, (query, args,))

    def execute(self, query, args=()):
        return self.writePool.apply(self.pool_execute, (query, args,))


    def usernameExists(self, username):
        res = self.query("SELECT uid FROM users WHERE username = ?", (username,))
        return (None if res is None else res[0]['uid'])

    def emailExists(self, emailAddress):
        res = self.query("SELECT uid FROM users WHERE email = ?", (emailAddress,))
        return (None if res is None else res[0]['uid'])

    def passwordCorrect(self, username, hpassword):
        res = self.query("SELECT uid FROM users WHERE username = ? AND hpassword = ?", (username, hpassword,))
        return (None if res is None else res[0]['uid'])



    def getRecovery(self, hrecovery):
        res = self.query("SELECT uid FROM users WHERE hrecovery = ?", (hrecovery,))
        return (None if res is None else res[0]['uid'])



    def userExists(self, uid):
        res = self.query("SELECT uid FROM users WHERE uid = ?", (uid,))
        return (None if res is None else uid)

    def postExists(self, pid):
        res = self.query("SELECT pid FROM posts WHERE pid = ?", (pid,))
        return (None if res is None else pid)

    def commentExists(self, cid):
        res = self.query("SELECT cid, owner FROM comments WHERE cid = ?", (cid,))
        return (None if res is None else res[0]['owner'])

    def imgExists(self, imgId):
        res = self.query("SELECT filename FROM images WHERE accessid = ?", (imgId,))
        return (None if res is None else res[0]['filename'])

    def tokenExists(self, token, type):
        res = self.query("SELECT owner FROM tokens WHERE value = ? AND type = ?", (token, type,))
        return (None if res is None else res[0]['owner'])

    def tokenData(self, token):
        res = self.query("SELECT data FROM tokens WHERE value = ?", (token,))
        return (None if res is None else res[0]['data'])


   
    def getPfp(self, uid):
        res1 = self.query("SELECT pfp FROM users WHERE uid = ?", (uid,))
        res2 = self.query("SELECT accessid FROM images WHERE imgid = ?", (res1[0]['pfp'],))
        # TODO: Debugging
        if res2 is None:
            return
        return res2[0]['accessid']

    def getFriends(self, uid): 
        res = self.query("SELECT user1, user2 FROM friendships WHERE (user1 = ? OR user2 = ?) AND accepted = 1", (uid, uid,)) 
        return [] if res is None else [tup['user1'] if tup['user1'] != uid else tup['user2'] for tup in res] 
    
    def getFriendReqsFromMe(self, uid): 
        res = self.query("SELECT user1, user2 FROM friendships WHERE user1 = ? AND accepted = 0", (uid,)) 
        return [] if res is None else [tup['user2'] for tup in res] 

    def getFriendReqsForMe(self, uid): 
        res = self.query("SELECT user1, user2 FROM friendships WHERE user2 = ? AND accepted = 0", (uid,)) 
        return [] if res is None else [tup['user1'] for tup in res] 

    def getPublicUserThumbnail(self, uid):
        res = self.query("SELECT uid, username, status, pfp FROM users WHERE uid = ?", (uid,))
        return None if res is None else res[0]

    def getPublicUser(self, uid):
        res = self.query("SELECT uid, username, status, suspended, pfp FROM users WHERE uid = ?", (uid,))
        info = res[0]
        res = self.query("SELECT pid, title FROM posts WHERE owner = ?", (uid,))
        info["posts"] = [] if res is None else [post for post in res]
        info["friends"] = {uid : info for uid, info in zip(self.getFriends(uid), map(self.getPublicUserThumbnail, self.getFriends(uid))) if uid is not None}
        return info

    def getUserLastAction(self, uid):        
        res = self.query("SELECT JULIANDAY('now')-JULIANDAY(lastaction) as delta FROM users WHERE uid=?", (uid,))
        if res is None:
            return None
        else:
            return 24*3600*res[0]['delta']

    def setUserLastAction(self, uid):
        self.execute("UPDATE users SET lastaction=CURRENT_TIMESTAMP WHERE uid=?", (uid,))

    def isUserSuspended(self, uid):
        res = self.query("SELECT suspended FROM users WHERE uid = ?", (uid,))
        return (res[0]['suspended'] == 1)
    
    def isUserConfirmed(self, uid):
        res = self.query("SELECT confirmed FROM users WHERE uid = ?", (uid,))
        return (res[0]['confirmed'] == 1)

    def isUserAdmin(self, uid):
        res = self.query("SELECT admin FROM users WHERE uid = ?", (uid,))
        return (res[0]['admin'] == 1)

    def getPrivateUser(self, uid, concise=False):
        res = self.query("SELECT uid, username, email, pfp, status, suspended, admin FROM users WHERE uid = ?", (uid,))
        info = res[0]
        if concise:
            return info
        res = self.query("SELECT pid, title FROM posts WHERE owner = ?", (uid,))
        info["posts"] = [] if res is None else [post for post in res]
        
        info["friends"] = {uid : info for uid, info in zip(self.getFriends(uid), map(self.getPublicUserThumbnail, self.getFriends(uid))) if uid is not None}
        info["fromyou"] = {uid : info for uid, info in zip(self.getFriendReqsFromMe(uid), map(self.getPublicUserThumbnail, self.getFriendReqsFromMe(uid))) if uid is not None}
        info["foryou"] = {uid : info for uid, info in zip(self.getFriendReqsForMe(uid), map(self.getPublicUserThumbnail, self.getFriendReqsForMe(uid))) if uid is not None}

        res = self.query("SELECT accessid, title FROM images WHERE owner = ?", (uid,))
        info["images"] = [] if res is None else [img for img in res]
        return info

    def getPostInfo(self, pid):
        res = self.query("SELECT P.pid, P.title, P.timestamp, P.owner, P.filename, U.username FROM posts P JOIN users U ON P.owner = U.uid WHERE P.pid = ?", (pid,))
        info = res[0]
        res = self.query("SELECT SUM(likes) as votes FROM votes WHERE postid = ?", (pid,))
        info["votes"] = 0 if res[0]['votes'] is None else res[0]['votes']
        res = self.query("SELECT U.uid, C.cid, C.content, C.timestamp, U.username FROM comments C JOIN users U on C.owner = U.uid WHERE post = ?", (pid,))
        info["comments"] = [] if res is None else [c for c in res]
        return info

    def getNumImages(self, uid):
        res = self.query("SELECT COUNT(*) as cnt FROM images WHERE owner = ?", (uid,))
        return res[0]['cnt']

    def getImageOwner(self, accessid):
        res = self.query("SELECT owner FROM images WHERE accessid = ?", (accessid,))
        return res[0]["owner"]

    def searchUser(self, substr):
        res = self.query("SELECT uid, username, pfp FROM users WHERE username LIKE '%' || ? || '%'", (substr,))
        return (None if res is None else [r for r in res])

    def searchPost(self, substr):
        res = self.query("SELECT P.pid, P.title, P.owner, U.username FROM posts P JOIN users U ON P.owner = U.uid WHERE P.title LIKE '%' || ? || '%' ORDER BY timestamp DESC", (substr,))
        return (None if res is None else [r for r in res])



    def createUser(self, email, username, hpassword, hrecovery, pfp):
        self.execute("INSERT INTO users (email, username, hpassword, hrecovery, pfp) VALUES (?, ?, ?, ?, ?)", (email, username, hpassword, hrecovery, pfp,))
        res = self.query("SELECT uid FROM users WHERE email = ?", (email,))
        return res[0]['uid']

    def verifyUser(self, uid):
        self.execute("UPDATE users SET confirmed = 1 WHERE uid = ?", (uid,))



    def createToken(self, uid, token, ttype, data=None):
        if data is None:
            self.execute("INSERT INTO tokens (owner, value, type) VALUES (?, ?, ?)", (uid, token, ttype,))
        else:
            self.execute("INSERT INTO tokens (owner, value, type, data) VALUES (?, ?, ?, ?)", (uid, token, ttype, data,))

    def expireToken(self, token):
        self.execute("DELETE FROM tokens WHERE value = ?", (token,))

    def expireAllSessions(self, uid):
        self.execute("DELETE FROM tokens WHERE owner = ? AND type='session'", (uid,))

    def getTokenAgeSeconds(self, token):
        res = self.query("SELECT JULIANDAY('now')-JULIANDAY(issued) as delta FROM tokens WHERE value=?", (token,))
        if res is None:
            return None
        else:
            return 24*3600*res[0]["delta"]



    def setStatus(self, uid, status):
        self.execute("UPDATE users SET status = ? WHERE uid = ?", (status, uid,))

    def setPicture(self, uid, accessid):
        self.execute("UPDATE users SET pfp = ? WHERE uid = ?", (accessid, uid,))

    def setEmail(self, uid, email):
        self.execute("UPDATE users SET email = ? WHERE uid = ?", (email, uid,))

    def setUsername(self, uid, username):
        self.execute("UPDATE users SET username = ? WHERE uid = ?", (username, uid,))

    def setPassword(self, uid, hpassword):
        self.execute("UPDATE users SET hpassword = ? WHERE uid = ?", (hpassword, uid,))

    def setBackup(self, uid, hbackup):
        self.execute("UPDATE users SET hrecovery = ? where uid = ?", (hbackup, uid,))


    def insertPost(self, uid, title, location):
        self.execute("INSERT INTO posts (owner, title, filename) VALUES (?, ?, ?)", (uid, title, location,))
        return self.query("SELECT pid FROM posts WHERE filename=?", (location,))[0]["pid"]

    def updatePost(self, pid, title):
        self.execute("UPDATE posts SET title=? WHERE pid=?", (title, pid,))

    def unlikePost(self, uid, pid):
        self.execute("DELETE FROM votes WHERE postid=? AND owner=?", (pid, uid,))

    def likePost(self, uid, pid):
        self.unlikePost(uid, pid)
        self.execute("INSERT INTO votes (owner, postid, likes) VALUES (?, ?, ?)", (uid, pid, 1))

    def dislikePost(self, uid, pid):
        self.unlikePost(uid, pid)
        self.execute("INSERT INTO votes (owner, postid, likes) VALUES (?, ?, ?)", (uid, pid, -1))

    def insertImage(self, uid, title, location, accessid):
        self.execute("INSERT INTO images (owner, title, filename, accessid) VALUES (?, ?, ?, ?)", (uid, title, location, accessid,))

    def insertComment(self, uid, pid, comment):
        self.execute("INSERT INTO comments (owner, post, content) VALUES (?, ?, ?)", (uid, pid, comment,))

    def deleteComment(self, cid):
        pid = self.query("SELECT post FROM comments WHERE cid=?", (cid,))[0]["post"]
        self.execute("DELETE FROM comments WHERE cid=?", (cid,))
        return pid



    def insertFriendReq(self, uid1, uid2):
        self.execute("UPDATE friendships SET accepted = 1 WHERE user1 = ? AND user2 = ?", (uid2, uid1,))
        res = self.query("SELECT accepted FROM friendships WHERE user1 = ? AND user2 = ?", (uid2, uid1,))
        if res is None:
            self.execute("INSERT INTO friendships (user1, user2) VALUES (?, ?)", (uid1, uid2,))

    def confirmFriendReq(self, uid1, uid2):
        self.insertFriendReq(uid1, uid2)

    def deleteFriendReq(self, uid1, uid2):
        self.execute("DELETE FROM friendships WHERE (user1 = ? AND user2 = ?) OR (user2 = ? AND user1 = ?)", (uid1, uid2, uid1, uid2,))



    def deletePost(self, pid):
        self.execute("DELETE FROM posts WHERE pid = ?", (pid,))
        self.execute("DELETE FROM comments WHERE post = ?", (pid,))
        self.execute("DELETE FROM votes WHERE postid = ?", (pid,))

    def deleteImage(self, accessid):
        self.execute("DELETE FROM images WHERE accessid = ?", (accessid,))

    def deleteUser(self, uid):
        self.execute("DELETE FROM users WHERE uid = ?", (uid,))
        self.execute("DELETE FROM tokens WHERE owner = ?", (uid,))
        self.execute("DELETE FROM posts WHERE owner = ?", (uid,))
        self.execute("DELETE FROM comments WHERE owner = ?", (uid,))
        self.execute("DELETE FROM images WHERE owner = ?", (uid,))
        self.execute("DELETE FROM reports WHERE owner = ?", (uid,))
        self.execute("DELETE FROM friendships WHERE user1 = ? OR user2 = ?", (uid, uid,))
        self.execute("DELETE FROM votes WHERE owner = ?", (uid,))



    def createBugReport(self, uid):
        self.execute("INSERT INTO reports (owner) VALUES (?)", (uid,))
        return self.query("SELECT rid FROM reports WHERE owner=? ORDER BY timestamp DESC", (uid,))[0]["rid"]



    def suspendUser(self, uid):
        self.execute("UPDATE users SET suspended = 1 WHERE uid = ?", (uid,))

    def unsuspendUser(self, uid):
        self.execute("UPDATE users SET suspended = 0 WHERE uid = ?", (uid,))

