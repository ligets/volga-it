import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .UserModel import UserModel


class RefreshSessionModel(Base):
    __tablename__ = 'refresh_session'

    refresh_token: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True)
    access_token: Mapped[str] = mapped_column()
    expires_in: Mapped[int]
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey(
        "users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    user: Mapped[UserModel] = relationship("UserModel", back_populates="refresh_sessions")
