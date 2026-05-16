from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.user import UserRead, UserEdit
from backend.app.services.user import UserService

router = APIRouter(tags=["Users"])

async def get_user_service(
        db: AsyncSession = Depends(get_db)
):
    return UserService(db)

@router.get("/users/me", response_model=UserRead)
async def user_check_self_info(
        user: UserRead = Depends(get_current_user),
):
    return user

@router.patch("/users/me", response_model=UserRead)
async def user_edit_self(
        data: UserEdit,
        user: UserRead = Depends(get_current_user),
        service: UserService = Depends(get_user_service),
):
    return await service.edit_user(
        uid=user.id,
        edit=data
    )

@router.delete("/users/me", status_code=204)
async def user_delete_self(
        user: UserRead = Depends(get_current_user),
        service: UserService = Depends(get_user_service),
):
    await service.delete_user(user.id)
    return Response(status_code=204)
