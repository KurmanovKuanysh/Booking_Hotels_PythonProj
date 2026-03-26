from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.booking import Booking
from backend.app.models.user import User
from backend.app.models.room import Room
from datetime import date, datetime
from fastapi import HTTPException

from backend.app.schemas.booking import BookingRead

ALLOWED_STATUSES = {"pending", "confirmed", "cancelled", "completed"}
ALLOWED_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["cancelled", "completed"],
    "cancelled": [],
    "completed": []
}

class BookingService:
    def __init__(self, session: Session):
        self.session = session

    def create_new_booking(
            self,
            r_id:int,
            guest_count: int,
            check_in: date,
            check_out: date,
            status: str,
            user_id: int,
            total_price: float
                ) -> Booking:
        booked_room = self.session.scalar(
            select(Booking)
            .where(Booking.r_id == r_id,
                   Booking.status.in_(["confirmed", "pending"]),
                   Booking.check_in < check_out,
                   Booking.check_out > check_in
                   )
        )
        if booked_room:
            raise HTTPException(status_code=409, detail="Room is already booked")
        if check_in > check_out:
            raise HTTPException(status_code=400, detail="Check-in date must be before check-out date")
        if status not in ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        if guest_count < 1:
            raise HTTPException(status_code=400, detail="Guest count must be at least 1")
        if total_price < 0:
            raise HTTPException(status_code=400, detail="Total price must be at least 0")
        room = self.session.scalar(select(Room).where(Room.id == r_id))
        if guest_count > room.capacity:
            raise HTTPException(status_code=400, detail="Guest count cannot exceed room capacity")
        new_booking = Booking(
            r_id=r_id,
            check_in=check_in,
            check_out=check_out,
            status=status,
            user_id=user_id,
            total_price=total_price
        )
        self.session.add(new_booking)
        self.session.commit()
        self.session.refresh(new_booking)
        return new_booking

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if self.get_booking_status(booking_id) in ("confirmed", "pending"):
            raise HTTPException(status_code=400, detail="Booking cannot be deleted, Booking status is not completed")
        self.session.delete(booking)
        self.session.commit()
        return True

    def get_booking_status(self, booking_id: int) -> str:
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking.status

    def cancel_booking(self, booking_id: int) -> bool:
        if self.update_booking_status(booking_id, "cancelled"):
            return True
        return False

    def confirm_booking(self, booking_id: int) -> bool:
        if self.update_booking_status(booking_id, "confirmed"):
            return True
        return False

    def complete_booking(self, booking_id: int) -> bool:
        if self.update_booking_status(booking_id, "completed"):
            return True
        return False

    def check_update_completed_bookings(self) -> list[BookingRead]:
        bookings = self.session.scalars(
            select(Booking)
            .where(Booking.check_out <= date.today(),
                   Booking.status.in_(["confirmed"]))
        ).all()
        if not bookings:
            return []
        changed = []
        for booking in bookings:
            booking.status = "completed"
            changed.append(booking)
        self.session.commit()
        return changed

    def has_confirmed_booking(self, user_id: int) -> bool:
        user = self.session.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        confirmed_bookings = self.session.scalars(
            select(Booking)
            .where(Booking.user_id == user_id,
                   Booking.status == "confirmed")
        ).all()

        return confirmed_bookings is not None

    def update_booking_status(self, booking_id: int, new_status: str) -> bool:
        if new_status.strip().lower() not in ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if new_status.strip().lower() not in ALLOWED_TRANSITIONS[booking.status]:
            raise HTTPException(status_code=400, detail="Invalid status transition")
        booking.status = new_status.strip().lower()
        self.session.commit()
        return True

    def get_booking_by_id(self, booking_id: int) -> Booking | None:
        return self.session.scalars(
            select(Booking)
            .where(Booking.id == booking_id)).first()

    def get_bookings_by_user_id(self, user_id: int) -> list[Booking]:
        return list(self.session.scalars(
            select(Booking)
            .where(Booking.user_id == user_id)
            ).all()
        )

    def get_bookings_by_user_email(self, email: str) -> list[Booking]:
        email = email.strip().lower()
        return list(self.session.scalars(
            select(Booking)
            .join(User, User.id == Booking.user_id)
            .where(User.email == email)
        ))

    def get_all_bookings(self) -> list[Booking]:
        return list(self.session.scalars(select(Booking)).all())

    def get_last_booking_of_user(self, user_id: int) -> Booking | None:
        booking = self.session.scalars(
                    select(Booking)
                    .where(Booking.user_id == user_id)
                    .order_by(Booking.id.desc())
        ).first()

        return booking

    def edit_booking(
            self,
            booking_id: int,
            r_id: int | None = None,
            check_in: date | None = None,
            check_out: date | None = None,
            status: str | None = None,
            user_id: int | None = None,

    ) -> Booking | None:
        booking = self.get_booking_by_id(booking_id)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        if r_id is not None:
            room = self.session.scalar(
                select(Room)
                .where(Room.id == r_id)
            )
            if room is None:
                raise HTTPException(status_code=404, detail="Room not found")
            booking.r_id = r_id

        if check_in and check_out:
            if check_in > check_out:
                raise HTTPException(status_code=400, detail="Check-in date must be before check-out date")
            booked_room = self.session.scalar(
                select(Booking)
                .where(Booking.r_id == booking.r_id ,
                       Booking.id != booking.id,
                       Booking.check_in < check_in,
                       Booking.check_out > check_out,
                       Booking.status.in_(["confirmed", "pending"])
                       )
            )
            if booked_room:
                raise HTTPException(status_code=400, detail="Room is already booked")
            booking.check_in = check_in
            booking.check_out = check_out

        if status:
            if status not in ALLOWED_STATUSES:
                raise HTTPException(status_code=400, detail="Invalid status")
            self.update_booking_status(booking.id, status)

        if user_id:
            user = self.session.scalar(select(User).where(User.id == user_id))
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            booking.user_id = user_id

        self.session.commit()
        self.session.refresh(booking)
        return booking

