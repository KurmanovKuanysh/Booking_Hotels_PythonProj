class AppError(Exception):
    pass

#==================== USER ====================
#REGISTER
class DuplicateEmailError(AppError):
    def __init__(self, email: str):
        self.email = email

#REGISTER END
class PasswordVerifyError(AppError):
    pass
#LOGIN
class InvalidLoginOrPasswordError(AppError):
    pass
#LOGIN END

#USER
class InvalidPasswordError(AppError):
    pass
class UserNotFoundError(AppError):
    pass
class InvalidNameLengthError(AppError):
    def __init__(self, name: str):
        self.name = name
#USER END

class InvalidStrLengthError(AppError):
    pass

class UserValidationError(AppError):
    pass

class InvalidUserRoleError(UserValidationError):
    pass
#====================USERS END====================

class RoomNotAvailableError(AppError):
    pass

class InvalidRoomTypeError(AppError):
    pass