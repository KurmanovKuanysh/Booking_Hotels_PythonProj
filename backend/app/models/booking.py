from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint, Enum, func, DateTime
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, date_, numeric_10_2
from datetime import datetime
import enum

class Status(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    r_id: Mapped[int_big] = mapped_column(ForeignKey("room.id"), nullable=False, index=True)
    check_in: Mapped[date_] = mapped_column(nullable=False)
    check_out: Mapped[date_] = mapped_column(nullable=False)
    status = mapped_column(Enum(Status), nullable=False)
    user_id: Mapped[int_big] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_price: Mapped[numeric_10_2] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    #relationship
    reviews = relationship("Review", back_populates="bookings")
    users = relationship("User", back_populates="bookings")
    rooms = relationship("Room", back_populates="bookings")

    __table_args__ = (
        CheckConstraint("status in ('pending', 'confirmed', 'cancelled', 'completed')", name="status_check"),
        CheckConstraint("check_in <= check_out", name="check_in_check"),
    )
