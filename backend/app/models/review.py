from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, DateTime, func, CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.utils.utils import int_big, numeric_10_2

class Review(Base):
    __tablename__ = "review"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    user_id: Mapped[int_big] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    booking_id: Mapped[int_big] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    hotel_id: Mapped[int_big] = mapped_column(
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    rating: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    comment: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    #relations
    bookings = relationship("Booking", back_populates="reviews")
    users = relationship("User", back_populates="reviews")
    hotels = relationship("Hotel", back_populates="reviews")

    def __repr__(self):
        return f"Review(id={self.id}, user_id={self.user_id}, booking_id={self.booking_id}, hotel_id={self.hotel_id}, rating={self.rating}, comment={self.comment}, created_at={self.created_at})"


