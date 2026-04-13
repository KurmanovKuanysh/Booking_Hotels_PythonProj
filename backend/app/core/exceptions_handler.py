from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.core.exceptions import (
    DuplicateEmailError,
    PasswordVerifyError,
    InvalidLoginOrPasswordError,
    InvalidPasswordError,
    UserNotFoundError,
    NotMatchedPasswords,
    NotFoundBookedRoomsError,
    NoPermissionRole, InvalidCityError, DatesConflictError, BookingNotFoundError, RoomNotAvailableError,
    InvalidStatusError, RoomNotFoundError, InvalidNumberError, RoomCapacityError, NoPermission, InvalidTokenError,
    HotelNotFoundError, ReviewNotFoundError, DuplicateReviewError, DuplicateRoomError, InvalidRoomNumberLength,
    RoomTypeNotFoundError, InvalidLengthError, BookingNotCompletedError
)

def register_errors_handlers(app: FastAPI):
    @app.exception_handler(DuplicateEmailError)
    def handle_user_duplicate_email_error(
            request: Request,
            exc: DuplicateEmailError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Email {exc.email} already registered"
            }
        )

    @app.exception_handler(PasswordVerifyError)
    def handle_password_verify_error(
            request: Request,
            exc: PasswordVerifyError
    ):
        return JSONResponse(
            status_code=401,
            content={
                "message": "Error verifying password, contact support!"
            }
        )

def login_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidLoginOrPasswordError)
    def handle_invalid_login_or_password_error(
            request: Request,
            exc: InvalidLoginOrPasswordError
    ):
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid email or password"
            }
        )

    @app.exception_handler(InvalidTokenError)
    def handle_invalid_token_error(
            request: Request,
            exc: InvalidTokenError
    ):
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid token"
            }
        )

def user_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidPasswordError)
    def handle_invalid_password_error(
            request: Request,
            exc: InvalidPasswordError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid password"
            }
        )

    @app.exception_handler(UserNotFoundError)
    def handle_user_not_found_error(
            request: Request,
            exc: UserNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "User not found"
            }
        )

    @app.exception_handler(NotMatchedPasswords)
    def handle_not_matched_passwords_error(
            request: Request,
            exc: NotMatchedPasswords
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "New Passwords do not match"
            }
        )
    @app.exception_handler(NoPermissionRole)
    def handle_user_permission_error(
            request: Request,
            exc: NoPermissionRole
    ):
        return JSONResponse(
            status_code=403,
            content={
                "message":"No permission granted"
            }
        )
    @app.exception_handler(NoPermission)
    def handle_user_permission_error(
            request: Request,
            exc: NoPermission
    ):
        return JSONResponse(
            status_code=403,
            content={}
        )

def booking_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(BookingNotCompletedError)
    def handle_booking_not_completed_error(
            request: Request,
            exc: BookingNotCompletedError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Booking not completed"
            }
        )

    @app.exception_handler(BookingNotFoundError)
    def handle_booking_not_found_error(
            request: Request,
            exc: BookingNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Booking not found"
            }
        )

    @app.exception_handler(NotFoundBookedRoomsError)
    def handle_not_found_booked_rooms_error(
            request: Request,
            exc: NotFoundBookedRoomsError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "No Booked rooms found"
            }
        )

    @app.exception_handler(DatesConflictError)
    def handle_dates_conflict_error(
            request: Request,
            exc: DatesConflictError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Dates conflict"
            }
        )
    @app.exception_handler(InvalidStatusError)
    def handle_user_permission_error(
            request: Request,
            exc: InvalidStatusError
    ):
        return JSONResponse(
            status_code=403,
            content={
                "message":"Invalid status"
            }
        )


def hotel_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidCityError)
    def handle_invalid_city_error(
            request: Request,
            exc: InvalidCityError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid city"
            }
        )

def room_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(RoomTypeNotFoundError)
    def handle_room_type_not_found_error(
            request: Request,
            exc: RoomTypeNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Room type not found"
            }
        )
    @app.exception_handler(InvalidRoomNumberLength)
    def handle_invalid_room_number_length(
            request: Request,
            exc: InvalidRoomNumberLength
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Room number must be max 10 char long"
            }
        )

    @app.exception_handler(DuplicateRoomError)
    def handle_duplicate_room_error(
            request: Request,
            exc: DuplicateRoomError
    ):
        return JSONResponse(
            status_code=409,
            content={
                "message": "Room already exists"
            }
        )

    @app.exception_handler(RoomNotAvailableError)
    def handle_room_not_available_error(
            request: Request,
            exc: RoomNotAvailableError
    ):
        return JSONResponse(
            status_code=409,
            content={
                "message": "Room not available"
            }
        )
    @app.exception_handler(RoomNotFoundError)
    def handle_room_not_found_error(
            request: Request,
            exc: RoomNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Room not found"
            }
        )
    @app.exception_handler(RoomCapacityError)
    def handle_room_capacity_error(
            request: Request,
            exc: RoomCapacityError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Room capacity exceeded"
            }
        )
def hotel_room_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(HotelNotFoundError)
    def handle_hotel_not_found_error(
            request: Request,
            exc: HotelNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Hotel not found"
            }
        )


def independent_errors_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidNumberError)
    def handle_invalid_number_error(
            request: Request,
            exc: InvalidNumberError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid number"
            }
        )
    @app.exception_handler(InvalidLengthError)
    def handle_invalid_length_error(
            request: Request,
            exc: InvalidLengthError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid length"
            }
        )

def review_errors_handling( app: FastAPI) -> None:
    @app.exception_handler(ReviewNotFoundError)
    def handle_review_not_found_error(
            request: Request,
            exc: ReviewNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Review not found"
            }
        )
    @app.exception_handler(DuplicateReviewError)
    def handle_duplicate_review_error(
            request: Request,
            exc: DuplicateReviewError
    ):
        return JSONResponse(
            status_code=409,
            content={
                "message": "Review already exists"
            }
        )