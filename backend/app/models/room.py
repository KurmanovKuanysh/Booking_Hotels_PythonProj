from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, numeric_10_2, text

class Room(Base):
    __tablename__ = "room"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    h_id: Mapped[int_big] = mapped_column(ForeignKey("hotel.id"), nullable=False )
    room_number: Mapped[text] = mapped_column(nullable=False)
    r_t_id: Mapped[int_big] = mapped_column(ForeignKey("room_type.id"), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    price_per_day: Mapped[numeric_10_2] = mapped_column(nullable=False)
    floor: Mapped[int] = mapped_column(nullable=False)

    #relationship
    room_type = relationship("RoomType", back_populates="room")
    hotel = relationship("Hotel", back_populates="room")
    booking = relationship("Booking", back_populates="room")


    __table_args__ = (
        CheckConstraint("capacity >= 0 and capacity <= 100", name="capacity_check"),
        CheckConstraint("price_per_day >= 0", name="price_per_day_check"),
        CheckConstraint("floor >= 0", name="floor_check"),
    )

