import sys
sys.path.insert(1, "../utilities")

from AgoraDatabaseManager import *

## These tests to be performed on an initially empty database.

dbman = AgoraDatabaseManager("../volumes/test.db")

assert dbman.userExists(1) is None
dbman.createUser("franklin@dyer.me", "frpzzd", "abc", "xyz")
assert dbman.userExists(1) == 1
dbman.createUser("theabecca@gmail.com", "althead", "def", "wxy")
assert dbman.userExists(2) == 2

dbman.insertFriendReq(2, 1)
assert dbman.getPublicUser(1)['friends'] == []
assert dbman.getPrivateUser(1)['foryou'] != []
assert dbman.getPrivateUser(2)['fromyou'] != []
dbman.confirmFriendReq(2, 1)
assert dbman.getPublicUser(1)['friends'] == []
dbman.confirmFriendReq(1, 2)
assert dbman.getPublicUser(1)['friends'] != []
assert dbman.getPrivateUser(1)['foryou'] == []

assert len(dbman.searchUser('d')) == 2
assert len(dbman.searchUser('zz')) == 1
assert len(dbman.searchUser('ead')) == 1
