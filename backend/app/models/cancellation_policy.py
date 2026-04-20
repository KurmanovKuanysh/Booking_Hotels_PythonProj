from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.utils.utils import int_big


class CancellationPolicy(Base):
    __tablename__ = "cancellation_policy"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hours_before: Mapped[int] = mapped_column(Integer, nullable=False)
    penalty_percent: Mapped[int] = mapped_column(Integer, nullable=False)

    #relationship
    hotels = relationship("Hotel", back_populates="policy")

    def __repr__(self):
        return f"CancellationPolicy(id={self.id}, name={self.name}, hours_before={self.hours_before}, penalty_percent={self.penalty_percent})"