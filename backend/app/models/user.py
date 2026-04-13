from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, str_100

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str_100] = mapped_column( nullable=False)
    email: Mapped[str_100] = mapped_column(nullable=False, unique=True)
    password: Mapped[str_100] = mapped_column(nullable=False)
    role: Mapped[str_100] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    #relationship
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("role IN ('ADMIN','S-ADMIN','USER')", name="role_check"),
    )