from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.deps import get_db, get_current_user
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingBase, BookingRead, BookingEdit, BookingNew
from backend.app.schemas.user import UserRead
from backend.app.services.booking import BookingService
from backend.app.models.booking import Status

router = APIRouter(tags=["Bookings"])

@router.post("/bookings", response_model=BookingBase)
def create_booking(
    booking: BookingNew,
    user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.is_active:
        service = BookingService(db)
        return service.create_new_booking(
            r_id=booking.r_id,
            guest_count=booking.guest_count,
            check_in=booking.check_in,
            check_out=booking.check_out,
            status="pending",
            user_id=user.id,
        )
    raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/bookings/me", response_model=list[BookingRead])
def get_user_bookings(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.get_bookings_by_user_id(user.id)

@router.patch("/bookings/{booking_id}", response_model=BookingRead)
def edit_booking_user(
        booking_id: int,
        booking: BookingEdit,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user)
):
    service = BookingService(db)

    edit = BookingEdit(
        check_in=booking.check_in,
        check_out=booking.check_out,
    )
    return service.edit_booking_user_side(
        user=user,
        booking_id=booking_id,
        edit=edit
    )
@router.patch("/bookings/{booking_id}/cancel", response_model=BookingRead)
def cancel_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user)
):
    service = BookingService(db)
    return service.cancel_booking(
        booking_id=booking_id,
        user=user,
    )