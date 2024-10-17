import uuid
from datetime import datetime

from sqlalchemy import UUID, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base_model import Base


class AppointmentModel(Base):
    __tablename__ = 'appointment'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    timetable_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("timetable.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    timetable: Mapped["TimetableModel"] = relationship("TimetableModel", back_populates='appointments')

