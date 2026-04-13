from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.utils.utils import int_big, numeric_10_2

class Review(Base):
    __tablename__ = "review"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    user_id: Mapped[int_big] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    booking_id: Mapped[int_big] = mapped_column(ForeignKey("bookings.id"), nullable=False, index=True)
    hotel_id: Mapped[int_big] = mapped_column(ForeignKey("hotels.id"), nullable=False, index=True)
    rating: Mapped[numeric_10_2] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    #relations
    bookings = relationship("Booking", back_populates="reviews")
    users = relationship("User", back_populates="reviews")
    hotels = relationship("Hotel", back_populates="reviews")

    __table_args__ = (
        CheckConstraint("rating >= 0 and rating <= 5", name="rating_check"),
    )

