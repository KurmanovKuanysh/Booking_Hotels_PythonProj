from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.booking import BookingRead, EditBookingStatus
from backend.app.schemas.user import UserRead, UserEdit
from sqlalchemy.orm import Session
from backend.app.services.booking import BookingService
from backend.app.services.user import UserService

router = APIRouter(tags=["Users"])

@router.get("/users/me")
def user_check_self_info(
        user: UserRead = Depends(get_current_user),
):
    return user

@router.patch("/users/me")
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


@router.get("/users/me/my-bookings", response_model=list[BookingRead])
def get_user_bookings(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = UserService(db)
    confirmed_bookings = service.get_user_bookings(user)
    return confirmed_bookings if confirmed_bookings else []

@router.patch("/users/me/my-bookings/cancel", status_code=204)
def cancel_booking(
        data: EditBookingStatus,
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    if data.status != "cancelled":
        raise HTTPException(status_code=400, detail="Invalid Status")
    return service.cancel_booking(booking_id=data.id, user=user)
