import datetime
import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, TIMESTAMP, String
from . import Base


class TimetableModel(Base):
    __tablename__ = 'timetable'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    hospitalId: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    doctorId: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    from_column: Mapped[datetime.datetime] = mapped_column("from", TIMESTAMP(timezone=True), nullable=False)
    to: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False)

    appointments: Mapped[list["AppointmentModel"]] = relationship(
        "AppointmentModel",
        back_populates="timetable",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
