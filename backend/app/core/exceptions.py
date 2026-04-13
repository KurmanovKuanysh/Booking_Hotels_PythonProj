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

class InvalidTokenError(AppError):
    pass
#LOGIN END

#USER
class NoPermissionRole(AppError):
    pass
class NoPermission(AppError):
    pass
class InvalidPasswordError(AppError):
    pass
class UserNotFoundError(AppError):
    pass
class InvalidNameLengthError(AppError):
    def __init__(self, name: str):
        self.name = name
class InvalidEmailLength(AppError):
    def __init__(self ,email: str):
        self.email = email
class NotMatchedPasswords(AppError):
    pass
class UserValidationError(AppError):
    pass
#USER END

#ROOM
class NotFoundBookedRoomsError(AppError):
    pass
class RoomNotFoundError(AppError):
    pass
class RoomCapacityError(AppError):
    pass
class DuplicateRoomError(AppError):
    pass
class InvalidRoomNumberLength(AppError):
    pass
class RoomTypeNotFoundError(AppError):
    pass
#ROOM END
#HOTEL
class HotelNotFoundError(AppError):
    pass
class InvalidCityError(AppError):
    def __init__(self, city: str):
        self.city = city
#HOTEL END

#BOOKING
class BookingNotFoundError(AppError):
    pass
class DatesConflictError(AppError):
    pass
class RoomNotAvailableError(AppError):
    pass
class InvalidStatusError(AppError):
    pass
class BookingNotCompletedError(AppError):
    pass
#BOOKING END

#REVIEW
class ReviewNotFoundError(AppError):
    pass
class DuplicateReviewError(AppError):
    pass

#REVIEWEND

#INDEPENDENT ERRORS
class InvalidNumberError(AppError):
    pass

class InvalidLengthError(AppError):
    pass
#INDEPENDENT ERRORS END