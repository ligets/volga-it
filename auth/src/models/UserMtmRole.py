from sqlalchemy import UUID, Table, ForeignKey, Column, Integer

from . import Base

user_mtm_role_table = Table(
    'user_mtm_role',
    Base.metadata,
    Column('user_id', UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.id'), nullable=False),
)

