from fastapi import status

class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Not correct Request"
class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"

class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated"

class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Forbidden"

class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Conflict"

class ValidationError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Validation failed"

# ==================== USER ====================

#REGISTER
class DuplicateEmailError(BadRequestError):
    detail = "User with this email already exists"

#LOGIN
class PasswordVerifyError(UnauthorizedError):
    detail = "Invalid credentials"

class InvalidLoginOrPasswordError(UnauthorizedError):
    detail = "Invalid login or password"

class InvalidTokenError(UnauthorizedError):
    detail = "Invalid token"

#USER
class NoPermissionRole(ForbiddenError):
    detail = "Your role doesn't have permission for this action"

class NoPermission(ForbiddenError):
    detail = "You don't have permission for this action"

class InvalidPasswordError(ValidationError):
    detail = "Invalid password"

class UserNotFoundError(NotFoundError):
    detail = "User not found"

class InvalidNameLengthError(ValidationError):
    detail = "Invalid name length"

class InvalidEmailLength(ValidationError):
    detail = "Invalid email length"

class NotMatchedPasswords(ValidationError):
    detail = "Passwords do not match"

class UserValidationError(ValidationError):
    detail = "User validation failed"


#ROOM

class NotFoundBookedRoomsError(NotFoundError):
    detail = "No booked rooms found"

class RoomNotFoundError(NotFoundError):
    detail = "Room not found"

class RoomCapacityError(ValidationError):
    detail = "Guest count exceeds room capacity"

class DuplicateRoomError(ConflictError):
    detail = "Room with this number already exists"

class InvalidRoomNumberLength(ValidationError):
    detail = "Invalid room number length"

class RoomTypeNotFoundError(NotFoundError):
    detail = "Room type not found"


#HOTEL

class HotelNotFoundError(NotFoundError):
    detail = "Hotel not found"

class InvalidCityError(ValidationError):
    detail = "Invalid city"

class HotelAlreadyExistsError(ConflictError):
    detail = "Hotel with this name/address already exists"

class HotelHaveBookingsError(ConflictError):
    detail = "Hotel have bookings"

#BOOKING

class BookingNotFoundError(NotFoundError):
    detail = "Booking not found"

class DatesConflictError(ValidationError):
    detail = "Invalid booking dates"

class RoomNotAvailableError(ConflictError):
    detail = "Room is not available for selected dates"

class InvalidStatusError(ValidationError):
    detail = "Invalid booking status"

class BookingNotCompletedError(ConflictError):
    detail = "Booking is not completed"
class BookingNotEditableError(ConflictError):
    detail = (
        "Booking is not editable. "
        "Only pending or confirmed bookings can be edited"
    )

#REVIEW

class ReviewNotFoundError(NotFoundError):
    detail = "Review not found"

class DuplicateReviewError(ConflictError):
    detail = "Review for this booking already exists"


#CANCELLATION
class PolicyHaveActiveHotelError(ConflictError):
    detail = (
        "Cancellation policy have active hotel. "
        "Please deactivate it before cancelling"
    )

#INDEPENDENT

class InvalidNumberError(ValidationError):
    detail = "Invalid number"

class InvalidLengthError(ValidationError):
    detail = "Invalid length"