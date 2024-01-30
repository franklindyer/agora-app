Here's a list of allowed database actions on the backend:
```
usernameExists     : RO check if username exists
emailExists        : RO check if email exists
passwordCorrect    : RO check if password is correct for username
getRecovery        : RO get user with given recovery code, if any

userExists         : RO check if user ID exists
postExists         : RO check if post ID exists
imgExists          : RO check is img ID exists

getPublicUser      : RO get public info of user by ID (name, pfp, friends, likes, posts)
getPrivateUser     : RO get private info of user by ID (public info + email, images)
searchUser         : RO get list of users with usernames like query
searchPost         : RO get list of posts with title like query

createToken        : RW create token of specific type for user
expireToken        : RW delete token of specific type for user

setStatus          : RW set status of a given user by ID
setPicture         : RW set profile picture of a given user by ID
setEmail           : RW set email of a given user by ID
setUsername        : RW set username of a given user by ID

insertPost         : RW create a new post entry with given info
insertImage        : RW create a new image with given info
insertComment      : RW create a comment from given user on given post by ID, with given content

insertFriendReq    : RW create a new friend request between users with given IDs
confirmFriendReq   : RW confirm an existing friend request between users with given IDs
deleteFriendReq    : RW remove an existing freind request between users with given IDs

deletePost         : RW delete a post with a given ID
deleteImage        : RW delete an image entry with a given ID
deleteUser         : RW delete a user with a given ID, as well as all of their posts, images, likes, comments etc.

suspendUser        : RW suspend user
unsuspendUser      : RW unsuspend user
```

Some notes about user actions:

```
createAccount   : EmailAddr -> Username -> Password -> CreateAccountToken
    POST to /createaccount with attributes "email", "username", "password"
confirmCreate   : CreateAccountToken -> BackupCode
    GET to /confirmaccount with query string argument "token"

login           : Username -> Password -> SessionToken
    POST to /login with attributes "username", "password"
logout          : SessionToken -> ()
    POST to /logout with cookie "session"

deleteAccount   : SessionToken -> Password -> DeleteAccountToken
    POST to /deleteaccount with cookie "session" and attribute "password"
comfirmDelete   : DeleteAccountToken -> ()
    GET to /confirmdelete with query string argument "token"

recoverAccount  : EmailAddr -> RecoveryToken
    POST to /recover with attribute "email"
backupRecover   : BackupCode -> EmailAddr -> RecoveryToken
    POST to /backup with attributes "code" and "email"
confirmRecover  : RecoveryToken -> Password -> ()
    POST to /confirmrecover with attributes "token" and "password"

getUser         : UserID -> UserPublicInfo
    GET to /profile/<uid>
getPost         : PostID -> PostInfo
    GET to /post/<pid>
getImage        : ImageID -> Image 
    GET to /img/<img_id>
searchUsers     : String -> [UserSummaryInfo]
    GET to /users with query string argument "query"
searchPosts     : String -> [PostSummaryInfo]
    GET to /posts with query string argument "query"

getMyUser       : SessionToken -> UserPrivateInfo

changeStatus    : SessionToken -> String -> ()
changePFP       : SessionToken -> ImageID -> ()
changeEmail     : SessionToken -> EmailAddr -> ChangeEmailToken
changeUsername  : SessionToken -> String -> ()

writePost       : SessionToken -> String -> String -> PostID
deletePost      : SessionToken -> PostID -> ()
uploadImage     : SessionToken -> String -> Image -> ImageID
deleteImage     : SessionToken -> ImageID -> ()
listImages      : SessionToken -> [(String, String)]

friendRequest   : SessionToken -> UserID -> ()
viewFriendReqs  : SessionToken -> [(String, UserID)]
acceptFriendReq : SessionToken -> UserID -> ()

comment         : SessionToken -> PostID -> String -> ()
likePost        : SessionToken -> PostID -> ()
dislikePost     : SessionToken -> PostID -> ()

bugReport       : SessionToken -> String -> ReportID

adminGetUser    : SessionToken -> UserID -> UserPrivateInfo
adminSuspend    : SessionToken -> UserID -> ()
adminUnsuspend  : SessionToken -> UserID -> ()
adminDelete     : SessionToken -> UserID -> Password -> ()
```

API responses will take the form of JSON. An error message will take this form:
```
{
    "success": 0,
    "message": "some error message goes here"
}
```
and a successful response will take this form:
```
{
    "success": 1,
    "data": {
        ...
    }
}
```
