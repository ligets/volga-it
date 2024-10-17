import uuid
from typing import Optional

from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import get_current_user
from src.accounts.schemas import UserDb
from .service import DoctorService

router = APIRouter()


@router.get("", response_model=list[UserDb])
@cache(expire=30)
async def get_doctors_list(
        nameFilter: Optional[str] = None,
        offset: int = Query(..., alias="from"),
        limit: int = Query(..., alias="count"),
        session: AsyncSession = Depends(db.get_async_session),
        user: str = Depends(get_current_user)
):
    return await DoctorService.get_list_doctors(
        nameFilter=nameFilter,
        offset=offset,
        limit=limit,
        session=session
    )


@router.get("/{id}", response_model=UserDb)
@cache(expire=30)
async def get_doctor_info(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        user: str = Depends(get_current_user)
):
    return await DoctorService.get_doctor(id, session)
