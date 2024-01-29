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
