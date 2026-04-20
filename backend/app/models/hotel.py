from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, ForeignKey, Text, String, Numeric, Integer
from backend.app.db.base import Base
from backend.app.utils.utils import int_big

class Hotel(Base):
    __tablename__ = "hotels"
    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    stars: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False, default=0.00,)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    rating_sum: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.00)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)

    policy_id: Mapped[int_big] = mapped_column(
        ForeignKey("cancellation_policy.id"),
        nullable=True
    )

    #relationship
    rooms = relationship("Room", back_populates="hotels", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="hotels", cascade="all, delete-orphan")
    policy = relationship("CancellationPolicy", back_populates="hotels")

    def __repr__(self):
        return f"Hotel(id={self.id}, name={self.name}, city={self.city}, address={self.address}, stars={self.stars}, description={self.description})"

