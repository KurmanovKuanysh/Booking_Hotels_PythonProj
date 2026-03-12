from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, text

class RoomType(Base):
    __tablename__ = "room_type"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    type_name: Mapped[text] = mapped_column(nullable=False)
    description: Mapped[text] = mapped_column(nullable=True)

    #relationship
    room = relationship("Room", back_populates="room_type")

    __table_args__ = (
        CheckConstraint("type_name <> '' AND type_name IN ('deluxe', 'family', 'general', 'suite', 'president')",
                        name="type_name_check"),
    )
