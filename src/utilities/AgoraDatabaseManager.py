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
        return self.conn.cursor()

    def query(self, query, args=(), one=False):
        cur = self.cur().execute(query, args)
        res = [x for x in cur.fetchall()]
        cur.close()
        return (res if len(res) > 0 else None)



    def usernameExists(self, username):
        res = self.query("SELECT uid FROM users WHERE username = ?", (username,))
        return (None if res is None else res[0]['uid'])

    def emailExists(self, emailAddress):
        res = self.query("SELECT uid FROM users WHERE email = ?", (emailAddress,))
        return (None if res is None else res[0]['uid'])

    def passwordCorrect(self, username, hpassword):
        res = self.query("SELECT uid FROM users WHERE username = ? AND password = ?", (username, hpassword,))
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
        res = self.query("SELECT imgid FROM images WHERE accessid = ?", (imgId))
        return (None if res is None else res[0]['imgid'])



    def getPublicUser(self, uid):
        res = self.query("SELECT uid, username, pfp, status, suspended FROM users WHERE uid = ?", (uid,))
        info = res[0]
        res = self.query("SELECT pid, title FROM posts WHERE owner = ?", (uid,))
        info["posts"] = [] if res is None else [post for post in res]
        res = self.query("SELECT user1, user2 FROM friendships WHERE (user1 = ? OR user2 = ?) AND accept1 = 1 AND accept2 = 1", (uid, uid,))
        info["friends"] = [] if res is None else [tup['user1'] if tup[0] != uid else tup['user2'] for tup in res] 
        return info

    def getPrivateUser(self, uid):
        res = self.query("SELECT uid, username, email, pfp, status, suspended, admin FROM users WHERE uid = ?", (uid,))
        info = res[0]
        res = self.query("SELECT pid, title FROM posts WHERE owner = ?", (uid,))
        info["posts"] = [] if res is None else [post for post in res]
        res = self.query("SELECT user1, user2 FROM friendships WHERE (user1 = ? OR user2 = ?) AND accept1 = 1 AND accept2 = 1", (uid, uid,))
        info["friends"] = [] if res is None else [tup['user1'] if tup['user1'] != uid else tup['user2'] for tup in res] 
        res = self.query("SELECT accessid, title FROM images WHERE owner = ?", (uid,))
        info["images"] = [] if res is None else [img for img in res]
        return info

    def getPostInfo(self, pid):
        res = self.query("SELECT pid, title, timestamp, owner FROM posts WHERE pid = ?", (pid,))
        info = res[0]
        res = self.query("SELECT uid, username FROM users WHERE uid = ?", info["owner"])
        info["owner"] = res[0]
        res = self.query("SELECT SUM(2*likes-1) FROM votes WHERE postid = ?", (pid,))
        info["votes"] = res[0]
        res = self.query("SELECT owner, content, timestamp FROM comments WHERE postid = ?", (pid,))
        info["comments"] = res[0]
        return info

    def searchUser(self, substr):
        res = self.query("SELECT uid, username FROM users WHERE username LIKE CONCAT('%', ?,'%')", (substr,))
        return (None if res is None else [r for r in res])

    def searchPost(self, substr):
        res = self.query("SELECT pid, title FROM posts WHERE title LIKE CONCAT('%', ?, '%') ORDER BY timestamp DESC", (substr,))
        return (None if res is None else [r for r in res])
