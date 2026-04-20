import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, String, Boolean, Enum
from backend.app.db.base import Base
from backend.app.utils.utils import int_big, str_100

class UserRole(enum.Enum):
    S_ADMIN = "S-ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", create_constraint=True),
        server_default=UserRole.USER.value,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    #relationship
    bookings = relationship("Booking", back_populates="users", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="users", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="users", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, role={self.role}, is_active={self.is_active})"