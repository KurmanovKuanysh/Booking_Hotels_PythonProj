from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.deps import get_db, get_current_user
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingBase, BookingRead, BookingEdit, BookingNew
from backend.app.schemas.user import UserRead
from backend.app.services.booking import BookingService

router = APIRouter(tags=["Bookings"])

@router.post("/new_booking", response_model=BookingBase)
def create_booking(
    guest_count: int,
    booking: BookingNew,
    user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.is_active:
        service = BookingService(db)
        return service.create_new_booking(
            r_id=booking.r_id,
            guest_count=guest_count,
            check_in=booking.check_in,
            check_out=booking.check_out,
            status=booking.status,
            user_id=user.id,
        )
    raise HTTPException(status_code=401, detail="Unauthorized")

@router.patch("/bookings/{booking_id}/edit", response_model=BookingRead)
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
        booking_id=booking_id,
        edit=edit
    )
@router.get("/bookings/my")
def get_my_bookings(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.get_bookings_by_user_id(user.id)
