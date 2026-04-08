from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.deps import get_db, validate_auth_user, get_current_user
from backend.app.core.exceptions import DuplicateEmailError, InvalidPasswordError, AppError
from backend.app.schemas.auth import TokenPair, RefreshRequest, LogOutRequest
from backend.app.schemas.user import UserRead, UserRegister, UserChangePassword, UserEdit
from backend.app.services.token import TokenService
from backend.app.services.user import UserService
from sqlalchemy.orm import Session
from backend.app.core.security import create_access_token, decode_refresh_token, create_refresh_token, verify_password
from backend.app.schemas.auth import RefreshTokenData, TokenData
REFRESH_TOKEN_EXPIRE_DAYS = 2
router = APIRouter(tags=["Authorization"])

@router.post("/auth/register", response_model=UserRead, status_code=201)
def create_user_account(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    service = UserService(db)

    if service.find_user_by_email(str(user_data.email)) is not None:
        raise DuplicateEmailError(email=str(user_data.email)) #BAD REQUEST
    new_user = service.register_user(
        user_data.name,
        str(user_data.email),
        user_data.password
    )
    return new_user
@router.post("/auth/login", response_model=TokenPair)
def login_user(
        user = Depends(validate_auth_user),
        db: Session = Depends(get_db)
):
    access_data = TokenData(
        sub=str(user.id),
        email=user.email,
        role=user.role,
        type="access"
    )
    access_token = create_access_token(
        data = access_data,
    )
    refresh_data = RefreshTokenData(
        sub=str(user.id),
        email=user.email,
        role=user.role,
        type="refresh"
    )
    refresh_token, expires_at = create_refresh_token(
        data=refresh_data,
    )
    token_service = TokenService(db)
    token_service.save_refresh_token(
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at
    )
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

@router.post("/auth/refresh", response_model=TokenPair)
def refresh_token(
        body: RefreshRequest,
        db: Session = Depends(get_db)
):
    token_service = TokenService(db)
    db_token = token_service.get_refresh_token(body.refresh_token)
    try:
        payload = decode_refresh_token(body.refresh_token)
    except Exception as e:
        raise e

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_service = UserService(db)
    user = user_service.get_user_by_id(db_token.user_id)

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    token_service.revoke_refresh_token(body.refresh_token)

    access_data = TokenData(sub=str(user.id), email=user.email, role=user.role, type="access")
    refresh_data = RefreshTokenData(sub=str(user.id), email=user.email, role=user.role, type="refresh")

    new_access_token = create_access_token(data=access_data,)
    new_refresh_token, new_token_expires_at = create_refresh_token(data=refresh_data,)

    token_service.save_refresh_token(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=new_token_expires_at
    )

    return TokenPair(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )

@router.post("/auth/logout")
def logout_user(
        body: LogOutRequest,
        db: Session = Depends(get_db)
):
    token_service = TokenService(db)
    token_service.revoke_refresh_token(body.refresh_token)
    return {"message": "Logged out"}

@router.patch("/auth/change-password", status_code=204)
def user_change_password(
        pass_data: UserChangePassword,
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = UserService(db)

    if not verify_password(
            pass_data.current_password,
            service.get_user_by_id(user.id).password
    ):
        raise InvalidPasswordError
    try:
        service.edit_user(
            uid=user.id,
            edit=UserEdit(
                password=pass_data.new_password
            )
        )
    except AppError as e:
        raise e
