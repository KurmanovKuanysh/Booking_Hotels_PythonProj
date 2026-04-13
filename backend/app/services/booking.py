from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from backend.app.core.exceptions import BookingNotFoundError, DatesConflictError, RoomNotAvailableError, \
    UserNotFoundError, InvalidStatusError, RoomNotFoundError, InvalidNumberError, RoomCapacityError, \
    NoPermission, BookingNotCompletedError
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
            raise RoomNotAvailableError
        if check_in > check_out:
            raise DatesConflictError
        if status not in ALLOWED_STATUSES:
            raise InvalidStatusError
        if guest_count < 1:
            raise InvalidNumberError
        room = self.session.scalar(select(Room).where(Room.id == r_id))
        if room is None:
            raise RoomNotFoundError
        total_price = room.price_per_day * (check_out - check_in).days
        if total_price < 0:
            raise InvalidNumberError
        if guest_count > room.capacity:
            raise RoomCapacityError
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
        if self.get_booking_status(booking_id) in ("confirmed", "pending"):
            raise BookingNotCompletedError
        self.session.delete(booking)
        self.session.commit()
        return True

    def delete_booking_cascade_admin(self, booking_id: int):
        booking = self.get_booking_by_id(booking_id)
        self.session.delete(booking)
        self.session.commit()
        return True

    def get_booking_status(self, booking_id: int) -> str:
        booking = self.get_booking_by_id(booking_id)
        return booking.status

    def cancel_booking(self, booking_id: int, user) -> bool:
        booking = self.session.scalar(
            select(Booking)
            .where(Booking.user_id == user.id,
                   Booking.id == booking_id,
                   Booking.status.in_(["confirmed", "pending"])
            )
        )
        if "cancelled" not in ALLOWED_TRANSITIONS[booking.status]:
            raise InvalidStatusError
        booking.status = "cancelled"
        booking.cancelled_at = datetime.now()
        self.session.commit()
        return True

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

    def has_confirmed_booking(self, user) -> bool:
        confirmed_bookings = self.session.scalars(
            select(Booking)
            .where(Booking.user_id == user.id,
                   Booking.status == "confirmed")
        ).all()

        return confirmed_bookings is not None

    def update_booking_status(self, booking_id: int, new_status: str) -> bool:
        if new_status.strip().lower() not in ALLOWED_STATUSES:
            raise InvalidStatusError
        booking = self.get_booking_by_id(booking_id)
        if new_status.strip().lower() not in ALLOWED_TRANSITIONS[booking.status]:
            raise InvalidStatusError
        booking.status = new_status.strip().lower()
        self.session.commit()
        return True

    def get_booking_by_id(self, booking_id: int) -> Booking | None:
        booking = self.session.scalars(
            select(Booking)
            .where(Booking.id == booking_id)).first()
        if not booking:
            raise BookingNotFoundError
        return booking

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

    def edit_booking_user_side(
            self,
            user,
            booking_id: int,
            edit,
            commit: bool = True
    ):
        booking = self.session.scalar(
            select(Booking)
            .where(Booking.id == booking_id)
        )
        if booking is None:
            raise BookingNotFoundError
        if booking.user_id != user.id:
            raise NoPermission
        new_check_in = edit.check_in if edit.check_in is not None else booking.check_in
        new_check_out = edit.check_out if edit.check_out is not None else booking.check_out
        new_r_id = edit.r_id if edit.r_id is not None else booking.r_id

        overlapping = self.session.scalars(
            select(Booking)
            .where(Booking.r_id == new_r_id,
                   Booking.id != booking.id,
                   Booking.check_in < new_check_out,
                   Booking.check_out > new_check_in,
                   Booking.status.in_(["confirmed", "pending"])
                   )
        )
        if overlapping is not None:
            raise DatesConflictError

        booked_room = self.session.scalar(
            select(Room)
            .join(Booking, Booking.r_id == Room.id)
            .where(Room.id == new_r_id,
                   Booking.check_in < new_check_out,
                   Booking.check_out > new_check_in,
                   )
            )

        if booked_room:
            raise RoomNotAvailableError
        booking.check_in = new_check_in
        booking.check_out = new_check_out
        booking.r_id = new_r_id

        if commit:
            self.session.commit()
            self.session.refresh(booking)

        return booking
    def edit_booking_admin_side(
            self,
            user,
            booking_id: int,
            edit
    ):
        booking = self.edit_booking_user_side(user, booking_id, edit, commit=False)

        new_user_id = edit.user_id if edit.user_id is not None else booking.user_id
        new_status = edit.status.strip().lower() if edit.status is not None else booking.status
        new_total_price = edit.total_price if edit.total_price is not None else booking.total_price

        user_exists = self.session.scalar(select(exists().where(User.id == edit.user_id)))
        if not user_exists:
            raise UserNotFoundError

        if new_status not in ALLOWED_STATUSES:
            raise InvalidStatusError

        booking.status = edit.status
        booking.user_id = new_user_id

        if new_total_price < 0:
            raise InvalidNumberError
        booking.total_price = edit.total_price

        self.session.commit()
        self.session.refresh(booking)
        return booking