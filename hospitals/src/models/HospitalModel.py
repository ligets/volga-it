import uuid
from typing import List
from sqlalchemy import UUID, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base
from .HospitalMtmRoom import hospital_mtm_room_table


class HospitalModel(Base):
    __tablename__ = 'hospitals'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    contactPhone: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    rooms: Mapped[List["RoomModel"]] = relationship(
        "RoomModel",
        secondary=hospital_mtm_room_table,
        back_populates="hospitals"
    )
