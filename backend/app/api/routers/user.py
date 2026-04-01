from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_current_user, get_db
from backend.app.core.exceptions import AppError, InvalidPasswordError
from backend.app.schemas.user import UserRead, UserEdit,UserChangePassword
from sqlalchemy.orm import Session
from backend.app.core.security import verify_password, hash_password
from backend.app.services.user import UserService

router = APIRouter(tags=["Users"])

@router.get("/users/me")
def user_check_self_info(
        user: UserRead = Depends(get_current_user),
):
    return {
        "email": user.email,
        "name": user.name,
    }

@router.patch("/users/me/password", status_code=204)
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

@router.patch("/users/me/edit")
def user_edit_self(
        data: UserEdit,
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.edit_user(
        uid=user.id,
        edit=data
    )

