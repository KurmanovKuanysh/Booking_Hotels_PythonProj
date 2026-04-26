from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, Integer, Numeric, String
from backend.app.db.base import Base
from backend.app.utils.utils import int_big

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    h_id: Mapped[int_big] = mapped_column(
        ForeignKey("hotels.id", ondelete="CASCADE",),
        nullable=False, index=True
    )
    room_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    r_t_id: Mapped[int_big] = mapped_column(
        ForeignKey("room_types.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    price_per_day: Mapped[float] = mapped_column(Numeric(10,2), nullable=False, index=True)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    #relationship
    room_types = relationship("RoomType", back_populates="rooms")
    hotels = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="rooms")


    def __repr__(self):
        return f"Room(id={self.id}, h_id={self.h_id}, room_number={self.room_number}, r_t_id={self.r_t_id}, capacity={self.capacity}, price_per_day={self.price_per_day}, floor={self.floor}, description={self.description})"


