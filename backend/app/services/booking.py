from decimal import Decimal

from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from backend.app.core.exceptions import BookingNotFoundError, DatesConflictError, RoomNotAvailableError, \
    UserNotFoundError, InvalidStatusError, RoomNotFoundError, InvalidNumberError, RoomCapacityError, \
    NoPermission, BookingNotCompletedError, BookingNotEditableError

from backend.app.models.booking import Booking
from backend.app.models.user import User
from backend.app.models.room import Room

from datetime import datetime
from backend.app.models.booking import Status
from backend.app.schemas.booking import BookingRead, BookingCreate

ALLOWED_TRANSITIONS = {
    Status.PENDING: [Status.CONFIRMED, Status.CANCELLED],
    Status.CONFIRMED: [Status.CANCELLED, Status.COMPLETED],
    Status.CANCELLED: [],
    Status.COMPLETED: [],
}

class BookingService:
    def __init__(self, session: Session):
        self.session = session

    def create_new_booking(
            self,
            user_id: int,
            data: BookingCreate
                ) -> Booking:
        booked_room = self.session.scalar(
            select(Booking)
            .where(Booking.r_id == data.r_id,
                   Booking.status.in_([Status.CONFIRMED, Status.PENDING]),
                   Booking.check_in < data.check_out,
                   Booking.check_out > data.check_in
                   )
        )
        if booked_room:
            raise RoomNotAvailableError

        room = self.session.scalar(select(Room).where(Room.id == data.r_id))
        if room is None:
            raise RoomNotFoundError

        if data.guest_count > room.capacity:
            raise RoomCapacityError

        nights = (data.check_out - data.check_in).days
        if nights <= 0:
            raise DatesConflictError

        total_price = room.price_per_day * nights


        new_booking = Booking(
            user_id=user_id,
            r_id=data.r_id,
            check_in=data.check_in,
            check_out=data.check_out,
            total_price=total_price,
            guest_count=data.guest_count
        )
        self.session.add(new_booking)
        self.session.commit()
        self.session.refresh(new_booking)
        return new_booking

    def get_booking_by_id(self, booking_id: int) -> Booking | None:
        booking = self.session.scalar(
            select(Booking)
            .where(Booking.id == booking_id))
        if booking is None:
            raise BookingNotFoundError
        return booking

    def get_booking_status(self, booking_id: int) -> str:
        booking = self.get_booking_by_id(booking_id)
        return str(booking.status)

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

    def has_confirmed_booking(self, user_id) -> bool:
        booking = self.session.scalar(
            select(Booking)
            .where(Booking.user_id == user_id,
                   Booking.status == Status.CONFIRMED)
        )

        return booking is not None

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.get_booking_by_id(booking_id)
        if booking.status in (Status.CONFIRMED, Status.PENDING):
            raise BookingNotCompletedError

        self.session.delete(booking)
        self.session.commit()
        return True

    def admin_delete_booking_cascade(self, booking_id: int):
        booking = self.get_booking_by_id(booking_id)
        self.session.delete(booking)
        self.session.commit()
        return True

    def update_booking_status(self, booking_id: int, new_status: Status) -> bool:
        booking = self.get_booking_by_id(booking_id)

        if new_status not in ALLOWED_TRANSITIONS[booking.status]:
            raise InvalidStatusError

        booking.status = new_status
        self.session.commit()
        return True

    def confirm_booking(self, booking_id: int) -> bool:
        return self.update_booking_status(booking_id, Status.CONFIRMED)

    def complete_booking(self, booking_id: int) -> bool:
        return self.update_booking_status(booking_id, Status.COMPLETED)

    def calculate_cancel_penalty(self, booking: Booking) -> tuple[Decimal, Decimal]:
        diff = booking.check_in - datetime.now()
        hours_before = diff.total_seconds() / 3600

        if hours_before > 48:
            penalty_percent = Decimal("0")
        elif hours_before > 24:
            penalty_percent = Decimal("0.2")
        else:
            penalty_percent = Decimal("0.5")

        penalty = booking.total_price * penalty_percent
        refund = booking.total_price - penalty
        if refund < 0:
            refund = Decimal("0")

        return penalty, refund

    def cancel_booking(self, booking_id: int, user_id: int) -> dict:
        booking = self.session.scalar(
            select(Booking)
            .where(
                Booking.id == booking_id,
                Booking.user_id == user_id,
                Booking.status.in_([Status.PENDING, Status.CONFIRMED]),
            )
        )
        if booking is None:
            raise BookingNotFoundError
        penalty, refund = self.calculate_cancel_penalty(booking)

        booking.status = Status.CANCELLED
        booking.cancelled_at = datetime.now()
        self.session.commit()
        self.session.refresh(booking)

        return {
            "message": "Booking cancelled successfully",
            "penalty": penalty,
            "refund": refund,
        }

    def check_update_completed_bookings(self) -> list[BookingRead]:
        bookings = self.session.scalars(
            select(Booking)
            .where(Booking.check_out <= datetime.today(),
                   Booking.status.in_([Status.CONFIRMED]))
        ).all()
        if not bookings:
            return []
        changed = []
        for booking in bookings:
            booking.status = Status.COMPLETED
            changed.append(booking)
        self.session.commit()
        return changed

    def edit_booking_user_side(
            self,
            user_id: int,
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
        if booking.user_id != user_id:
            raise NoPermission
        if booking.status not in (Status.PENDING, Status.CONFIRMED):
            raise BookingNotEditableError

        new_check_in = edit.check_in if edit.check_in is not None else booking.check_in
        new_check_out = edit.check_out if edit.check_out is not None else booking.check_out
        new_r_id = edit.r_id if edit.r_id is not None else booking.r_id

        room_exists = self.session.scalar(select(exists().where(Room.id == new_r_id)))
        if not room_exists:
            raise RoomNotFoundError

        overlapping = self.session.scalar(
            select(Booking)
            .where(Booking.r_id == new_r_id,
                   Booking.id != booking.id,
                   Booking.check_in < new_check_out,
                   Booking.check_out > new_check_in,
                   Booking.status.in_([Status.CONFIRMED, Status.PENDING])
                   )
        )
        if overlapping:
            raise DatesConflictError


        booking.check_in = new_check_in
        booking.check_out = new_check_out
        booking.r_id = new_r_id

        if commit:
            self.session.commit()
            self.session.refresh(booking)

        return booking

    def edit_booking_admin_side(self, user_id: int, booking_id: int, edit) -> Booking:
        booking = self.edit_booking_user_side(user_id, booking_id, edit, commit=False)
        if edit.user_id is not None:
            user_exists = self.session.scalar(
                select(exists().where(User.id == edit.user_id))
            )
            if not user_exists:
                raise UserNotFoundError
            booking.user_id = edit.user_id

        if edit.status is not None:
            booking.status = edit.status
        if edit.total_price is not None:
            if edit.total_price < 0:
                raise InvalidNumberError
            booking.total_price = edit.total_price

        self.session.commit()
        self.session.refresh(booking)
        return booking
