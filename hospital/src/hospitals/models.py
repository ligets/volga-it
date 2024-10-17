import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Table, ForeignKey, Column, String, Boolean
from src.base_model import Base

hospital_mtm_room_table = Table(
    'hospital_mtm_room',
    Base.metadata,
    Column('hospital_id', UUID, ForeignKey('hospitals.id', ondelete="CASCADE"), nullable=False),
    Column('rooms_id', UUID, ForeignKey('rooms.id', ondelete="CASCADE"), nullable=False),
)


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
