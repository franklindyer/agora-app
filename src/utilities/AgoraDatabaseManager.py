import sqlite3

class AgoraDatabaseManager:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = sqlite3.Row

    def cur(self):
        return self.conn.cursor()

    def query(self, query, args=(), one=False):
        cur = self.cur().execute(query, args)
        res = cur.fetchall()
        cur.close()
        return (res if len(res) > 0 else None)



    def usernameExists(self, username):
        res = self.query("SELECT * FROM users WHERE username = ?", (username,))
        return (None if res is None else res[0]['uid'])

    def emailExists(self, emailAddress):
        res = self.query("SELECT * FROM users WHERE email = ?", (emailAddress,))
        return (None if res is None else res[0]['uid'])
