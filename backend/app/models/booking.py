from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint, Enum
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, text, date_, date_t, numeric_10_2
from datetime import datetime
import enum

class Status(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    r_id: Mapped[int_big] = mapped_column(ForeignKey("room.id"), nullable=False)
    check_in: Mapped[date_] = mapped_column(nullable=False)
    check_out: Mapped[date_] = mapped_column(nullable=False)
    status = mapped_column(Enum(Status), nullable=False)
    user_id: Mapped[int_big] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_price: Mapped[numeric_10_2] = mapped_column(nullable=False)
    created_at: Mapped[date_t] = mapped_column(nullable=False, default=datetime.utcnow)

    #relationship
    user = relationship("User", back_populates="booking")
    room = relationship("Room", back_populates="booking")

    __table_args__ = (
        CheckConstraint("status in ('pending', 'confirmed', 'cancelled', 'completed')", name="status_check"),
        CheckConstraint("check_in <= check_out", name="check_in_check"),
    )
