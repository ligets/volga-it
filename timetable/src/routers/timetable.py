from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import validate_user_role
from src.schemas.timetable import TimetableCreate, TimetableResponse
from src.services.timetable import TimetableService

router = APIRouter()


@router.post('', response_model=TimetableResponse)
async def create_timetable(
        timetable: TimetableCreate,
        session: AsyncSession = Depends(db.get_async_session),
        user_info: dict = Depends(validate_user_role(['Admin', 'Manager']))
):
    return await TimetableService.create_timetable(timetable, session, user_info.get('token'))
