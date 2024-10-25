import uuid

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.dao import UserDAO
from src.accounts.models import UserModel, RoleModel


class DoctorService:
    @classmethod
    async def get_doctor(cls, doctor_id: uuid.UUID, session: AsyncSession):
        doctor = await UserDAO.find_one_or_none(session, UserModel.id == doctor_id)

        if doctor is None or 'Doctor' not in [role.name for role in doctor.roles]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

        return doctor

    @classmethod
    async def get_list_doctors(
            cls,
            nameFilter: str,
            offset: int,
            limit: int,
            session: AsyncSession
    ):
        filters = [RoleModel.name == 'Doctor', UserModel.is_deleted == False]
        if nameFilter:
            filters.append(func.concat(UserModel.firstName, " ", UserModel.lastName).ilike(f"%{nameFilter}%"))

        return await UserDAO.fild_all(
            session,
            *filters,
            offset=offset,
            limit=limit,
        )
