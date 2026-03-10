from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.booking import Booking
from backend.app.models.user import User
from datetime import date

ALLOWED_STATUSES = {"pending", "confirmed", "cancelled", "completed"}

class BookingService:
    def __init__(self, session: Session):
        self.session = session

    def create_new_booking(self,r_id:int,check_in: date, check_out: date,status: str,user_id: int) -> Booking:
        if check_in > check_out:
            raise ValueError("Check-in date must be before check-out date")
        if status not in ALLOWED_STATUSES:
            raise ValueError("Invalid status")


        new_booking = Booking(
            r_id=r_id,
            check_in=check_in,
            check_out=check_out,
            status=status,
            user_id=user_id
        )
        self.session.add(new_booking)
        self.session.commit()
        self.session.refresh(new_booking)
        return new_booking

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

    def check_update_completed_bookings(self) -> bool:
        bookings = self.session.scalars(
            select(Booking)
            .where(Booking.check_out <= date.today(),
                   Booking.status.not_in(["completed","canceled"]))
        ).all()
        for booking in bookings:
            booking.status = "completed"
        self.session.commit()
        return True


    def update_booking_status(self, booking_id: int, status: str) -> bool:
        if status.strip().lower() not in ALLOWED_STATUSES:
            raise ValueError("Invalid status")
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return False
        booking.status = status.strip().lower()
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
                    # .limit(1)
        ).first()
        if booking:
            booking.status = "confirmed"

            self.session.commit()
            self.session.refresh(booking)

        return booking
