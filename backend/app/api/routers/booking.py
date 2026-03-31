from fastapi import APIRouter, Depends
from backend.app.api.deps import get_db
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingBase, BookingRead, BookingEdit
from backend.app.services.booking import BookingService

router = APIRouter(tags=["Bookings"])

@router.post("/bookings", response_model=BookingBase)
def create_booking(
    guest_count: int,
    booking: BookingBase,
    db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.create_new_booking(
        r_id=booking.r_id,
        guest_count=guest_count,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status=booking.status,
        user_id=booking.user_id,
        total_price=booking.total_price
    )
@router.get("/bookings", response_model=list[BookingRead])
def get_bookings(db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_all_bookings()
@router.patch("/bookings/{booking_id}/edit", response_model=BookingRead)
def edit_booking(
        booking_id: int,
        booking: BookingEdit,
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.edit_booking(
        booking_id=booking_id,
        r_id=booking.r_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status=booking.status,
        user_id=booking.user_id
    )
@router.get("/bookings/{booking_id}", response_model=BookingRead)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_booking_by_id(booking_id)

@router.get("/bookings/{booking_id}/status", response_model=str)
def get_booking_status(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_booking_status(booking_id)
@router.delete("/bookings/{booking_id}", response_model=bool)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.delete_booking(booking_id)
@router.get("/bookings/my")
def get_my_bookings(db: Session = Depends(get_db)):
    service = BookingService(db)
    return
@router.get("/bookings/user/{user_id}", response_model=list[BookingRead])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_bookings_by_user_id(user_id)

