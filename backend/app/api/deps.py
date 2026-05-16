from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import AsyncSessionLocal
from fastapi import HTTPException, Depends, Request
from backend.app.schemas.user import UserRead
from backend.app.models.user import UserRole

from backend.app.services.user import UserService
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer, OAuth2PasswordRequestForm
)

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def validate_auth_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    service = UserService(db)

    user = await service.login_user(
        email=form_data.username,
        password=form_data.password
    )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user

def get_current_token_payload(request: Request):
    return request.state.user_payload

async def get_current_user(
        token: str = Depends(http_bearer),
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_db)
) -> UserRead:
    uid = payload.get("sub")
    if uid is None:
        raise HTTPException(status_code=401, detail="token invalid (sub missing)")

    service = UserService(db)
    user = await service.get_user_by_id(int(uid))

    if user is not None:
        return user
    raise HTTPException(status_code=401, detail="token invalid (user not found)")

async def get_current_user_admin(
        user: UserRead = Depends(get_current_user),
) -> UserRead:
    if user.role in [UserRole.ADMIN,UserRole.S_ADMIN]:
        return user
    raise HTTPException(status_code=403, detail="Not an admin")

