import uuid
from datetime import datetime

from sqlalchemy import UUID, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from src.base_model import Base


class HistoryModel(Base):
    __tablename__ = 'history'
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    pacientId: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    hospitalId: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    doctorId: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    room: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[str] = mapped_column(String)
    date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
