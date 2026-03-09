from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint
from app.db.base import Base
from app.utils.utils import int_big, numeric_10_2, text

class Hotel(Base):
    __tablename__ = "hotel"
    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[text] = mapped_column(nullable=False )
    city: Mapped[text] = mapped_column(nullable=False)
    address: Mapped[text] = mapped_column(nullable=False)
    stars: Mapped[numeric_10_2] = mapped_column(nullable=False)

    #relationship
    room = relationship("Room", back_populates="hotel")

    __table_args__ = (
        CheckConstraint("stars >= 0 and stars <= 5", name="stars_check"),
    )

