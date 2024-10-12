from typing import Union, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseDAO, UpdateSchemaType
from src.schemas.appointments import CreateAppointmentsDB
from ..models.appointments import AppointmentModel


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
