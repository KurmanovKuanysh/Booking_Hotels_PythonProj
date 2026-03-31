from backend.app.core.exceptions import InvalidLoginOrPasswordError
from backend.app.db.session import SessionLocal
from fastapi import Form, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import verify_password
from backend.app.schemas.user import UserRead

from backend.app.services.user import UserService
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer
)
from backend.app.core.security import decode_access_token
from jose import JWTError

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        db: Session = Depends(get_db)
):
    service = UserService(db)

    user = service.get_user_by_email(username)
    if user is None:
        raise InvalidLoginOrPasswordError
    if verify_password(
            plain_password=password,
            hashed_password=user.password
    ):
        return user

    raise InvalidLoginOrPasswordError
def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode_access_token(
            token=token
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"token invalid {e}")
    if payload is None:
        raise HTTPException(status_code=401, detail="token invalid")
    return payload

def get_current_user(
        payload: dict = Depends(get_current_token_payload),
        db: Session = Depends(get_db)
) -> UserRead:
    uid = payload.get("sub")
    if uid is None:
        raise HTTPException(status_code=401, detail="token invalid (sub missing)")
    service = UserService(db)
    user = service.get_user_by_id(int(uid))
    if user is not None:
        return user
    raise HTTPException(status_code=401, detail="token invalid (user not found)")

def get_current_user_admin(
        user: UserRead = Depends(get_current_user),
) -> UserRead:
    if user.role == "ADMIN":
        return user
    raise HTTPException(status_code=403, detail="Not an admin")

def get_current_active_user(
        user: UserRead = Depends(get_current_user),
) -> UserRead:
    if user.is_active:
        return user
    raise HTTPException(status_code=403, detail="Inactive user")
