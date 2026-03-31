from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.deps import get_db, get_current_user
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingBase, BookingRead, BookingEdit, BookingNew
from backend.app.schemas.user import UserRead
from backend.app.services.booking import BookingService

router = APIRouter(tags=["Bookings"])

@router.post("/new_book", response_model=BookingBase)
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
            total_price=booking.total_price
        )
    raise HTTPException(status_code=401, detail="Unauthorized")

@router.patch("/bookings/{booking_id}/edit", response_model=BookingRead)
def edit_booking(
        booking_id: int,
        booking: BookingEdit,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user)
):
    service = BookingService(db)
    return service.edit_booking(
        booking_id=booking_id,
        r_id=booking.r_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status=booking.status,
        user_id=user.id
    )
@router.get("/bookings/{booking_id}", response_model=BookingRead)
def get_booking_by_id(
    booking_id: int,
    user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BookingService(db)
    if user.role == "admin" or user.id == service.get_booking_by_id(booking_id).user_id:
        return service.get_booking_by_id(booking_id)
    raise HTTPException(status_code=401, detail="Not Allowed")

@router.get("/bookings/{booking_id}/status", response_model=str)
def get_booking_status(
        booking_id: int,
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    if user.role == "admin" or user.id == service.get_booking_by_id(booking_id).user_id:
        return service.get_booking_status(booking_id)
    raise HTTPException(status_code=401, detail="Not Allowed")

@router.get("/bookings/my")
def get_my_bookings(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.get_bookings_by_user_id(user.id)
@router.get("/bookings/user/{user_id}", response_model=list[BookingRead])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_bookings_by_user_id(user_id)

