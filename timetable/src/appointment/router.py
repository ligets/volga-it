import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import get_current_user
from src.appointment.service import AppointmentsService

router = APIRouter()


@router.delete('/{id}')
async def delete_appointment(
        id: uuid.UUID,
        user: dict = Depends(get_current_user),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AppointmentsService.delete_appointment(user, id, session)

