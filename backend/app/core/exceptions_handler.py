from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.core.exceptions import (
    DuplicateEmailError,
    PasswordVerifyError,
    InvalidLoginOrPasswordError,
    InvalidPasswordError,
    UserNotFoundError,
    InvalidNameLengthError,
)

def register_errors_handlers(app: FastAPI):
    @app.exception_handler(DuplicateEmailError)
    def handle_user_duplicate_email_error(
            request: Request,
            exc: DuplicateEmailError
    ):
        return JSONResponse(
            status_code=409,
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
    @app.exception_handler(InvalidNameLengthError)
    def handle_invalid_name_length_error(
            request: Request,
            exc: InvalidNameLengthError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid name length"
                "Name must be between 2 and 100 characters long"
            }
        )