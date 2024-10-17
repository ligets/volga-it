from typing import Optional

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.base_dao import BaseDAO
from src.timetable.model import TimetableModel
from src.timetable.schemas import TimetableCreate


class TimetableDAO(BaseDAO[TimetableModel, TimetableCreate, TimetableCreate]):
    model = TimetableModel

    @classmethod
    async def fild_all(
            cls,
            session: AsyncSession,
            *filters,
            offset: int = 0,
            limit: int = 100,
            **filter_by
    ):
        stmt = (
            select(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
            .order_by(asc(TimetableModel.from_column))
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ) -> Optional[TimetableModel]:
        stmt = select(cls.model).filter(*filters).filter_by(**filter_by).options(selectinload(cls.model.appointments))
        result = await session.execute(stmt)
        return result.scalars().one_or_none()
