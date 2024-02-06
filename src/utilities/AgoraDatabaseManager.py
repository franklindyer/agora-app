import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class AgoraDatabaseManager:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = dict_factory

    def cur(self):
        # Making a new connection each time is only a temporary band-aid, not a long-term fix.
        # It solves the problem of a single connection being unshareable between threads, and Flask being multithreaded.
        # The ultimate solution will be to create a "job queue" as part of this class.
        self.conn = sqlite3.connect(self.dbname)
        self.conn.row_factory = dict_factory
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def query(self, query, args=(), one=False):
        cur = self.cur().execute(query, args)
        res = [x for x in cur.fetchall()]
        cur.close()
        return (res if len(res) > 0 else None)

    def execute(self, query, args=(), one=False):
        cur = self.cur().execute(query, args)
        cur.close()
        self.commit()



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

    def imgExists(self, imgId):
        res = self.query("SELECT filename FROM images WHERE accessid = ?", (imgId,))
        return (None if res is None else res[0]['filename'])

    def tokenExists(self, token, type):
        res = self.query("SELECT owner FROM tokens WHERE value = ? AND type = ?", (token, type,))
        return (None if res is None else res[0]['owner'])



    def getPublicUser(self, uid):
        res = self.query("SELECT uid, username, pfp, status, suspended FROM users WHERE uid = ?", (uid,))
        info = res[0]
        res = self.query("SELECT pid, title FROM posts WHERE owner = ?", (uid,))
        info["posts"] = [] if res is None else [post for post in res]
        res = self.query("SELECT F.user1, F.user2, U1.username as username1, U2.username as username2 FROM friendships F join users U1 on U1.uid = F.user1 join users U2 on U2.uid = F.user2 WHERE (user1 = ? OR user2 = ?) AND accepted = 1", (uid, uid,))
        info["friends"] = [] if res is None else [(tup['user1'], tup['username1']) if tup['user1'] != uid else (tup['user2'], tup['username2']) for tup in res] 
        return info

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
        
        res = self.query("SELECT user1, user2 FROM friendships WHERE (user1 = ? OR user2 = ?) AND accepted = 1", (uid, uid,))
        info["friends"] = [] if res is None else [tup['user1'] if tup['user1'] != uid else tup['user2'] for tup in res]
        res = self.query("SELECT user2 FROM friendships WHERE user1 = ? AND accepted = 0", (uid,))
        info["fromyou"] = [] if res is None else [r['user2'] for r in res]
        res = self.query("SELECT user1 FROM friendships WHERE user2 = ? AND accepted = 0", (uid,))
        info["foryou"] = [] if res is None else [r['user1'] for r in res]

        res = self.query("SELECT accessid, title FROM images WHERE owner = ?", (uid,))
        info["images"] = [] if res is None else [img for img in res]
        return info

    def getPostInfo(self, pid):
        res = self.query("SELECT P.pid, P.title, P.timestamp, P.owner, P.filename, U.username FROM posts P JOIN users U ON P.owner = U.uid WHERE P.pid = ?", (pid,))
        info = res[0]
        res = self.query("SELECT SUM(2*likes-1) as votes FROM votes WHERE postid = ?", (pid,))
        info["votes"] = 0 if res[0]['votes'] is None else res[0]['votes']
        res = self.query("SELECT U.uid, C.content, C.timestamp, U.username FROM comments C JOIN users U on C.owner = U.uid WHERE post = ?", (pid,))
        info["comments"] = [] if res is None else [c for c in res]
        return info

    def getNumImages(self, uid):
        res = self.query("SELECT COUNT(*) as cnt FROM images WHERE owner = ?", (uid,))
        return res[0]['cnt']

    def getImageOwner(self, accessid):
        res = self.query("SELECT owner FROM images WHERE accessid = ?", (accessid,))
        return res[0]["owner"]

    def searchUser(self, substr):
        res = self.query("SELECT uid, username FROM users WHERE username LIKE '%' || ? || '%'", (substr,))
        return (None if res is None else [r for r in res])

    def searchPost(self, substr):
        res = self.query("SELECT pid, title FROM posts WHERE title LIKE '%' || ? || '%' ORDER BY timestamp DESC", (substr,))
        return (None if res is None else [r for r in res])



    def createUser(self, email, username, hpassword, hrecovery):
        self.execute("INSERT INTO users (email, username, hpassword, hrecovery) VALUES (?, ?, ?, ?)", (email, username, hpassword, hrecovery,))
        res = self.query("SELECT uid FROM users WHERE email = ?", (email,))
        return res[0]['uid']

    def verifyUser(self, uid):
        self.execute("UPDATE users SET confirmed = 1 WHERE uid = ?", (uid,))



    def createToken(self, uid, token, ttype):
        self.execute("INSERT INTO tokens (owner, value, type) VALUES (?, ?, ?)", (uid, token, ttype))

    def expireToken(self, token):
        self.execute("DELETE FROM tokens WHERE value = ?", (token,))



    def setStatus(self, uid, status):
        self.execute("UPDATE users SET status = ? WHERE uid = ?", (status, uid,))

    def setPicture(self, uid, imgid):
        self.execute("UPDATE users SET pfp = ? WHERE uid = ?", (imgid, uid,))

    def setEmail(self, uid, email):
        self.execute("UPDATE users SET email = ? WHERE uid = ?", (email, uid,))

    def setUsername(self, uid, username):
        self.execute("UPDATE users SET username = ? WHERE uid = ?", (username, uid,))



    def insertPost(self, uid, title, location):
        self.execute("INSERT INTO posts (owner, title, filename) VALUES (?, ?, ?)", (uid, title, location,))

    def insertImage(self, uid, title, location, accessid):
        self.execute("INSERT INTO images (owner, title, filename, accessid) VALUES (?, ?, ?, ?)", (uid, title, location, accessid,))

    def insertComment(self, uid, pid, comment):
        self.execute("INSERT INTO comments (owner, post, content) VALUES (?, ?, ?)", (uid, pid, comment,))



    def insertFriendReq(self, uid1, uid2):
        self.execute("UPDATE friendships SET accepted = 1 WHERE user1 = ? AND user2 = ?", (uid2, uid1,))
        res = self.query("SELECT accepted FROM friendships WHERE user1 = ? AND user2 = ?", (uid1, uid2,))
        if res is None:
            self.execute("INSERT INTO friendships (user1, user2) VALUES (?, ?)", (uid1, uid2,))

    def confirmFriendReq(self, uid1, uid2):
        self.insertFriendReq(uid1, uid2)

    def deleteFriendReq(self, uid1, uid2):
        self.execute("DELETE FROM friendships WHERE (user1 = ? AND user2 = ?) OR (user2 = ? AND user1 = ?)", (uid1, uid2, uid1, uid2,))



    def deletePost(self, pid):
        self.execute("DELETE FROM posts WHERE pid = ?", (pid,))

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



    def suspendUser(self, uid):
        self.execute("UPDATE users SET suspended = 1 WHERE uid = ?", (uid,))

    def unsuspendUser(self, uid):
        self.execute("UPDATE users SET suspended = 0 WHERE uid = ?", (uid,))

