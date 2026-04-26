import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Enum
from backend.app.db.base import Base
from backend.app.utils.utils import int_big

def get_enum_values(enum_class):
    result = []
    for member in enum_class:
        result.append(member.value)
    return result       #берем values из енум

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
        Enum(UserRole, name="user_role", create_constraint=True, values_callable=get_enum_values ),
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