from fastapi import APIRouter, Depends
from backend.app.api.deps import get_db, validate_auth_user
from backend.app.core.exceptions import DuplicateEmailError
from backend.app.schemas.auth import Token
from backend.app.schemas.user import  UserRead,UserRegister
from backend.app.services.user import UserService
from sqlalchemy.orm import Session
from backend.app.core.security import create_access_token
from datetime import timedelta

REFRESH_TOKEN_EXPIRE_DAYS = 2
router = APIRouter(tags=["Authorization"])

@router.post("/auth/register-admin", response_model=UserRead, status_code=201)
def create_user_account(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    service = UserService(db)

    if service.get_user_by_email(str(user_data.email)) is not None:
        raise DuplicateEmailError(email=str(user_data.email))

    new_user = service.register_user(
        name=user_data.name,
        email=str(user_data.email),
        password=user_data.password,
        role="ADMIN"
    )
    return new_user
@router.post("/auth/register", response_model=UserRead, status_code=201)
def create_user_account(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    service = UserService(db)

    if service.get_user_by_email(str(user_data.email)) is not None:
        raise DuplicateEmailError(email=user_data.email)

    new_user = service.register_user(
        user_data.name,
        str(user_data.email),
        user_data.password
    )
    return new_user
@router.post("/auth/login", response_model=Token)
def login_user(
        user = Depends(validate_auth_user),
):
    access_token = create_access_token(
        data={
            'sub':str(user.id),
            'email':user.email,
        }
    )
    refresh_token = create_access_token(
        data={
            'sub':str(user.id),
            'email':user.email,
        },
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )