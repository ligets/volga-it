import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import validate_token
from src.dependencies import get_current_admin
from src.schemas.HospitalsSchemas import HospitalCreate, HospitalUpdate, HospitalResponse, \
    HospitalCreateResponse
from src.schemas.RoomsSchemas import RoomResponse
from src.services.HospitalService import HospitalService

router = APIRouter()


@router.get('', response_model=list[HospitalResponse])
async def get_list_hospitals(
        offset: int = Query(..., alias='from'),
        limit: int = Query(..., alias='count'),
        session: AsyncSession = Depends(db.get_async_session),
        valid_token: dict = Depends(validate_token)
):
    return await HospitalService.get_list_hospitals(offset, limit, session)


@router.get('/{id}', response_model=HospitalResponse)
async def get_hospital_info(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        valid_token: dict = Depends(validate_token)
):
    return await HospitalService.get_hospital(id, session)


@router.get('/{id}/Rooms', response_model=list[RoomResponse])
async def get_hospital_rooms(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        valid_token: dict = Depends(validate_token)
):
    return await HospitalService.get_list_rooms(id, session)


@router.post('', response_model=HospitalCreateResponse)
async def create_hospital(
        data: HospitalCreate,
        session: AsyncSession = Depends(db.get_async_session),
        admin: dict = Depends(get_current_admin)
):
    return await HospitalService.create_hospital(data, session)


@router.put('/{id}', response_model=HospitalCreateResponse)
async def update_hospital(
        id: uuid.UUID,
        data: HospitalUpdate,
        session: AsyncSession = Depends(db.get_async_session),
        admin: dict = Depends(get_current_admin)
):
    return await HospitalService.update_hospital(id, data, session)


@router.delete('/{id}')
async def delete_hospital(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        admin: dict = Depends(get_current_admin)
):
    return await HospitalService.delete_hospital(id, session)


