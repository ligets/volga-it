import uuid
from typing import List
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base
from .HospitalMtmRoom import hospital_mtm_room_table


class RoomModel(Base):
    __tablename__ = 'rooms'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    hospitals: Mapped[List["HospitalModel"]] = relationship(
        "HospitalModel",
        secondary=hospital_mtm_room_table,
        back_populates="rooms",
        cascade="all, delete",
        passive_deletes=True
    )
