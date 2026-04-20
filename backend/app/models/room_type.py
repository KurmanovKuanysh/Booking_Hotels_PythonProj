from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, Text, String
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, text

class RoomType(Base):
    __tablename__ = "room_types"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    #relationship
    rooms = relationship("Room", back_populates="room_types")

    def __repr__(self):
        return f"RoomType(id={self.id}, type_name={self.type_name}, description={self.description})"
