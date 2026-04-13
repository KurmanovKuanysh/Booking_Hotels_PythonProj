from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, numeric_10_2, text

class Hotel(Base):
    __tablename__ = "hotels"
    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[text] = mapped_column(nullable=False )
    city: Mapped[text] = mapped_column(nullable=False)
    address: Mapped[text] = mapped_column(nullable=False)
    stars: Mapped[numeric_10_2] = mapped_column(nullable=False)
    description: Mapped[text] = mapped_column(nullable=True)

    rating_sum: Mapped[numeric_10_2] = mapped_column(default=0)
    rating_count: Mapped[int_big] = mapped_column(default=0)

    #relationship
    rooms = relationship("Room", back_populates="hotels", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="hotels", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("stars >= 0 and stars <= 5", name="stars_check"),
    )

