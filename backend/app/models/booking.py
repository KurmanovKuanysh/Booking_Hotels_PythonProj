from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, func, DateTime, Numeric, Integer
from backend.app.db.base import Base
from backend.app.utils.utils import int_big
from datetime import datetime
import enum

class Status(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

def get_enum_values(enum_class):
    result = []
    for member in enum_class:
        result.append(member.value)
    return result       #берем values из енум

class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int_big] = mapped_column(primary_key=True)
    user_id: Mapped[int_big] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    r_id: Mapped[int_big] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    check_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    check_out: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    status:Mapped[Status] = mapped_column(
        Enum(Status, name="booking_status", create_constraint=True, values_callable=get_enum_values),
        nullable=False, default=Status.PENDING
    )
    total_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    guest_count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    #relationship
    reviews = relationship("Review", back_populates="bookings")
    users = relationship("User", back_populates="bookings")
    rooms = relationship("Room", back_populates="bookings")
    transactions = relationship("Transaction", back_populates="bookings")

    def __repr__(self):
        return f"Booking(id={self.id}, check_in={self.check_in}, check_out={self.check_out}, status={self.status}, user_id={self.user_id}, total_price={self.total_price}, created_at={self.created_at}, cancelled_at={self.cancelled_at})"
