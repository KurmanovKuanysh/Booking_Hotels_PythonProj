from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.booking import Booking
from backend.app.models.user import User
from backend.app.models.room import Room
from datetime import date

ALLOWED_STATUSES = {"pending", "confirmed", "cancelled", "completed"}

class BookingService:
    def __init__(self, session: Session):
        self.session = session

    def create_new_booking(
            self,
            r_id:int,
            check_in: date,
            check_out: date,
            status: str,
            user_id: int) -> Booking:
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

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if self.get_booking_status(booking_id) in ("completed", "pending"):
            raise ValueError("Booking cannot be deleted")
        self.session.delete(booking)
        self.session.commit()
        return True

    def get_booking_status(self, booking_id: int) -> str:
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
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

    def check_update_completed_bookings(self) -> bool:
        bookings = self.session.scalars(
            select(Booking)
            .where(Booking.check_out <= date.today(),
                   Booking.status.not_in(["completed","cancelled"]))
        ).all()
        for booking in bookings:
            booking.status = "completed"
        self.session.commit()
        return True

    def has_confirmed_booking(self, user_id: int) -> bool:
        user = self.session.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise ValueError("User not found")
        confirmed_bookings = self.session.scalars(
            select(Booking)
            .where(Booking.user_id == user_id,
                   Booking.status == "confirmed")
        ).all()

        return confirmed_bookings is not None

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
        # if booking:
        #     booking.status = "confirmed"
        #
        #     self.session.commit()
        #     self.session.refresh(booking)
        return booking

    def edit_booking(self, edit: dict) -> Booking:
        if "id" not in edit:
            raise ValueError("Booking id is required")
        booking = self.get_booking_by_id(edit["id"])
        if booking is None:
            raise ValueError("Booking not found")

        if "r_id" in edit and edit["r_id"] is not None:
            room = self.session.scalar(
                select(Room)
                .where(Room.id == edit["r_id"])
            )
            if room is None:
                raise ValueError("Room not found")
            booking.r_id = edit["r_id"]

        if ("check_in" in edit and edit["check_in"] is not None) and ("check_out" in edit and edit["check_out"] is not None):
            if edit["check_in"] > edit["check_out"]:
                raise ValueError("Check-in date must be before check-out date")
            booked_room = self.session.scalar(
                select(Booking)
                .where(Booking.r_id == booking.r_id ,
                       Booking.id != booking.id,
                       Booking.check_in < edit["check_in"],
                       Booking.check_out > edit["check_out"],
                       Booking.status.in_(["confirmed", "pending"])
                       )
            )
            if booked_room:
                raise ValueError("Room is already booked for the selected dates")
            booking.check_in = edit["check_in"]
            booking.check_out = edit["check_out"]

        if "status" in edit and edit["status"] is not None:
            if edit["status"] not in ALLOWED_STATUSES:
                raise ValueError("Invalid status")
            self.update_booking_status(booking.id, edit["status"])

        if "user_id" in edit and edit["user_id"] is not None:
            user = self.session.scalar(select(User).where(User.id == edit["user_id"]))
            if user is None:
                raise ValueError("User not found")
            booking.user_id = edit["user_id"]

        self.session.commit()
        self.session.refresh(booking)
        return booking

