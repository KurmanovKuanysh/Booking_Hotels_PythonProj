import enum
from datetime import datetime

from sqlalchemy import Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.utils.utils import int_big

class Type(enum.Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    PENALTY = "penalty"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    booking_id: Mapped[int_big] = mapped_column(
        ForeignKey("bookings.id"),
        nullable=False, index=True
    )
    payment_id: Mapped[int_big] = mapped_column(
        ForeignKey("payments.id"),
        nullable=True, index=True
    )
    type = mapped_column(Enum(Type), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    #relationship
    bookings = relationship("Booking", back_populates="transactions")
    payment = relationship("Payment", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, booking_id={self.booking_id}, type={self.type}, created_at={self.created_at})"
