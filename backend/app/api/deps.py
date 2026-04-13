from backend.app.db.session import SessionLocal
from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from backend.app.schemas.user import UserRead

from backend.app.services.user import UserService
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer, OAuth2PasswordRequestForm
)

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_auth_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    service = UserService(db)

    user = service.login_user(
        email=form_data.username,
        password=form_data.password
    )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user

def get_current_token_payload(request: Request):
    return request.state.user_payload

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
    if user.role in ["ADMIN","S-ADMIN"]:
        return user
    raise HTTPException(status_code=403, detail="Not an admin")

