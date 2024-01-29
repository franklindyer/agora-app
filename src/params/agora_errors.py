class AgoraException(Exception):
    pass

# Errors pertaining to account creation, login, and recovery
class AgoraEInvalidEmail(AgoraException):
    pass
class AgoraEInvalidUsername(AgoraException):
    pass
class AgoraEInvalidPassword(AgoraException):
    pass
class AgoraEInvalidToken(AgoraException):
    pass

# Errors pertaining to user-uploaded content
class AgoraEBadImage(AgoraException):
    pass
class AgoraEInvalidTitle(AgoraException):
    pass
class AgoraEInvalidReport(AgoraException):
    pass

# Authentication errors
class AgoraEIncorrectCreds(AgoraException):
    pass
class AgoraENonexistentEmail(AgoraException):
    pass
class AgoraEIncorrectCode(AgoraException):
    pass

# Errors pertaining to retrieval of public content
class AgoraENoSuchUser(AgoraException):
    pass
class AgoraENoSuchPost(AgoraException):
    pass
class AgoraENoSuchImage(AgoraException):
    pass

# Access control errors
class AgoraENotLoggedIn(AgoraException):
    pass
class AgoraENotAuthorized(AgoraException):
    pass


