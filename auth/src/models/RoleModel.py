from . import Base
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .UserMtmRole import user_mtm_role_table


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
