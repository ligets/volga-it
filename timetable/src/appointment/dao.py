from typing import Union, Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.base_dao import BaseDAO, UpdateSchemaType, ModelType
from src.appointment.schemas import CreateAppointmentsDB
from src.appointment.model import AppointmentModel


class AppointmentDAO(BaseDAO[AppointmentModel, CreateAppointmentsDB, None]):
    model = AppointmentModel

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ):
        raise NotImplementedError("Обновление не поддерживается в этом DAO")

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ) -> Optional[AppointmentModel]:
        stmt = select(cls.model).filter(*filters).filter_by(**filter_by).options(selectinload(cls.model.timetable))
        result = await session.execute(stmt)
        return result.scalars().one_or_none()
