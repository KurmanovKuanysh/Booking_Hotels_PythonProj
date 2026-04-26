from fastapi import APIRouter, Depends

from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.user import UserRead, UserEdit
from sqlalchemy.orm import Session
from backend.app.services.user import UserService

router = APIRouter(tags=["Users"])

@router.get("/users/me", response_model=UserRead)
def user_check_self_info(
        user: UserRead = Depends(get_current_user),
):
    return user

@router.patch("/users/me", response_model=UserRead)
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

@router.delete("/users/me", status_code=204)
def user_delete_self(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.delete_user(user.id)
