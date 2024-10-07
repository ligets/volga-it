from sqlalchemy import UUID, Table, ForeignKey, Column
from . import Base

hospital_mtm_room_table = Table(
    'hospital_mtm_room',
    Base.metadata,
    Column('hospital_id', UUID, ForeignKey('hospitals.id', ondelete="CASCADE"), nullable=False),
    Column('rooms_id', UUID, ForeignKey('rooms.id', ondelete="CASCADE"), nullable=False),
)

