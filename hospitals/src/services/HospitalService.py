import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.daos.HospitalsDAO import HospitalsDAO
from src.models.HospitalModel import HospitalModel
from src.schemas.HospitalsSchemas import HospitalCreate, HospitalCreateDB, HospitalUpdateDB


class HospitalService:
    @classmethod
    async def create_hospital(cls, data: HospitalCreate, session: AsyncSession):
        return await HospitalsDAO.add(
            session,
            HospitalCreateDB(**data.dict())
        )

    @classmethod
    async def get_hospital(cls, hospital_id: uuid.UUID, session: AsyncSession):
        hospital = await HospitalsDAO.find_one_or_none(session, id=hospital_id)
        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hospital not found.')
        return hospital

    @classmethod
    async def get_list_rooms(cls, hospital_id: uuid.UUID, session: AsyncSession):
        return await HospitalsDAO.get_rooms(session, id=hospital_id)

    @classmethod
    async def get_list_hospitals(cls, offset: int, limit: int, session: AsyncSession):
        return await HospitalsDAO.find_all(session, offset=offset, limit=limit)

    @classmethod
    async def delete_hospital(cls, hospital_id: uuid.UUID, session: AsyncSession):
        await HospitalsDAO.delete(session, id=hospital_id)

    @classmethod
    async def update_hospital(cls, hospital_id: uuid.UUID, data: HospitalCreate, session: AsyncSession):
        hospital = await HospitalsDAO.update(
            session,
            HospitalModel.id == hospital_id,
            obj_in=HospitalUpdateDB(
                **data.dict()
            )
        )
        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hospital not found.')
        return hospital
