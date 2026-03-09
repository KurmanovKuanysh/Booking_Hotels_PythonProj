from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from app.db.base import Base
from app.utils.utils import int_big, text, date_


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    r_id: Mapped[int_big] = mapped_column(ForeignKey("room.id"), nullable=False)
    check_in: Mapped[date_] = mapped_column(nullable=False)
    check_out: Mapped[date_] = mapped_column(nullable=False)
    status: Mapped[text] = mapped_column(nullable=False)
    user_id: Mapped[int_big] = mapped_column(ForeignKey("users.id"), nullable=False)

    #relationship
    user = relationship("User", back_populates="booking")
    room = relationship("Room", back_populates="booking")

    __table_args__ = (
        CheckConstraint("check_in <= check_out AND check_in >= CURRENT_DATE", name="check_in_check"),
        CheckConstraint("status in ('pending', 'confirmed', 'cancelled', 'completed')", name="status_check"),
    )
