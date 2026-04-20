from backend.app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean, DateTime
from datetime import datetime
from backend.app.utils.utils import int_big


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int_big] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int_big] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    token: Mapped[str] = mapped_column(String(512), nullable=False, index=True, unique=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean,default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    #relationship
    users = relationship("User", back_populates="refresh_tokens")