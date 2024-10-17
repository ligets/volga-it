import uuid
from typing import List

from sqlalchemy import String, Boolean, UUID, Table, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base_model import Base


user_mtm_role_table = Table(
    'user_mtm_role',
    Base.metadata,
    Column('user_id', UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.id'), nullable=False),
)


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstName: Mapped[str] = mapped_column(String(50), nullable=False)
    lastName: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    roles: Mapped[List["RoleModel"]] = relationship(
        "RoleModel",
        secondary=user_mtm_role_table,
        back_populates="users"
    )
    refresh_sessions: Mapped[List["RefreshSessionModel"]] = relationship(
        "RefreshSessionModel",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class RoleModel(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    users: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary=user_mtm_role_table,
        back_populates="roles",
        cascade="all, delete",
        passive_deletes=True
    )
