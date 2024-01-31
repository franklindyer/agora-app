Here's a list of allowed database actions on the backend:
```
usernameExists     : RO check if username exists
emailExists        : RO check if email exists
passwordCorrect    : RO check if password is correct for username
getRecovery        : RO get user with given recovery code, if any

userExists         : RO check if user ID exists
postExists         : RO check if post ID exists
imgExists          : RO check is img ID exists
tokenExists        : RO check if a token is valid and of a given type

getPublicUser      : RO get public info of user by ID (name, pfp, friends, likes, posts)
isUserSuspended    : RO determine if user is suspended
isUserConfirmed    : RO determine is user is confirmed
isAdmin            : RO determine if user is admin
getPrivateUser     : RO get private info of user by ID (public info + email, images)
getPostInfo        : RO get post title and filename (to be replaced with content) as well as likes/dislikes and comments
searchUser         : RO get list of users with usernames like query
searchPost         : RO get list of posts with title like query

createUser         : RW create user with given username, email, password, recovery code
verifyUser         : RW change user to "confirmed"

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
confirmCreate   : CreateAccountToken -> BackupCode

login           : Username -> Password -> SessionToken
logout          : SessionToken -> ()

deleteAccount   : SessionToken -> Password -> DeleteAccountToken
comfirmDelete   : DeleteAccountToken -> ()

recoverAccount  : EmailAddr -> RecoveryToken
backupRecover   : BackupCode -> EmailAddr -> RecoveryToken
confirmRecover  : RecoveryToken -> Password -> ()

getUser         : UserID -> UserPublicInfo
getPost         : PostID -> PostInfo
getImage        : ImageID -> Image 
searchUsers     : String -> [UserSummaryInfo]
searchPosts     : String -> [PostSummaryInfo]

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

