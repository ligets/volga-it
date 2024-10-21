import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from src.hospitals.dao import HospitalsDAO
from src.dependencies import delete_timetable_hospital
from .models import HospitalModel
from .schemas import HospitalCreate, HospitalCreateDB, HospitalUpdateDB


class HospitalService:
    @classmethod
    async def create_hospital(cls, data: HospitalCreate, session: AsyncSession):
        return await HospitalsDAO.add(
            session,
            HospitalCreateDB(**data.model_dump())
        )

    @classmethod
    async def get_hospital(cls, hospital_id: uuid.UUID, session: AsyncSession):
        hospital = await HospitalsDAO.find_one_or_none(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            )
        )
        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hospital not found.')
        return hospital

    @classmethod
    async def get_list_rooms(cls, hospital_id: uuid.UUID, session: AsyncSession):
        return await HospitalsDAO.get_rooms(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            )
        )

    @classmethod
    async def get_list_hospitals(cls, offset: int, limit: int, session: AsyncSession):
        return await HospitalsDAO.find_all(session, HospitalModel.is_deleted == False, offset=offset, limit=limit)

    @classmethod
    async def delete_hospital(cls, hospital_id: uuid.UUID, session: AsyncSession):
        hospital = await HospitalsDAO.update(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            ),
            obj_in={'is_deleted': True}
        )
        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hospital not found.')
        await delete_timetable_hospital(hospital_id)

    @classmethod
    async def update_hospital(cls, hospital_id: uuid.UUID, data: HospitalCreate, session: AsyncSession):
        hospital = await HospitalsDAO.update(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            ),
            obj_in=HospitalUpdateDB(
                **data.model_dump()
            )
        )
        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hospital not found.')
        return hospital
