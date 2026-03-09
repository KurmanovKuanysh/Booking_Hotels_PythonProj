from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint
from app.db.base import Base
from app.utils.utils import int_big, str_100

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str_100] = mapped_column( nullable=False)
    email: Mapped[str_100] = mapped_column(nullable=False, unique=True)
    password: Mapped[str_100] = mapped_column(nullable=False)
    role: Mapped[str_100] = mapped_column(nullable=False)

    #relationship
    booking = relationship("Booking", back_populates="user")


    __table_args__ = (
        CheckConstraint("role IN ('ADMIN', 'USER')", name="role_check"),
    )