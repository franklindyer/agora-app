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
