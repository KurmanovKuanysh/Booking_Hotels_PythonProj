from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.utils.utils import int_big


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    method_id: Mapped[int_big] = mapped_column(
        ForeignKey("payment_methods.id", ondelete="CASCADE"),
        nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    is_paid: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    #relationship
    payment_methods = relationship("PaymentMethod", back_populates="payment")
    transactions = relationship("Transaction", back_populates="payment")

    def __repr__(self):
        return f"Payment(id={self.id}, method_id={self.method_id}, amount={self.amount}, is_paid={self.is_paid}, created_at={self.created_at}, updated_at={self.updated_at})"

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    #relationship
    payment = relationship("Payment", back_populates="payment_methods")

    def __repr__(self):
        return f"PaymentMethod(id={self.id}, name={self.name})"