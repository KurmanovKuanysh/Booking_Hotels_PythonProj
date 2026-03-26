class AppError(Exception):
    pass

class UserNotFoundError(AppError):
    pass

class InvalidLoginOrPasswordError(AppError):
    pass

class DuplicateEmailError(AppError):
    pass

class UserValidationError(AppError):
    pass

class InvalidUserRoleError(UserValidationError):
    pass

class RoomNotAvailableError(AppError):
    pass

class InvalidRoomTypeError(AppError):
    pass