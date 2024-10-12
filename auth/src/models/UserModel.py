import uuid
from typing import List

from sqlalchemy import String, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .UserMtmRole import user_mtm_role_table


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
