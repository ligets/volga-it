import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.daos.UserDAO import UserDAO
from src.models.UserModel import UserModel
from src.models.RoleModel import RoleModel
from src.schemas.UserSchemas import UserUpdate, UserUpdateDB, UserUpdateAdmin, \
    UserCreate, UserCreateAdmin, UserCreateDB
from src.utils import get_password_hash


class UserService:
    @classmethod
    async def create_user(
            cls,
            data: UserCreate | UserCreateAdmin,
            session: AsyncSession
    ):
        return await UserDAO.add(
            session,
            UserCreateDB(
                **data.dict(exclude={"password"}),
                hashed_password=get_password_hash(data.password)
            )
        )

    @classmethod
    async def get_user(cls, user_id: uuid.UUID, session: AsyncSession) -> Optional[any]:
        user = await UserDAO.find_one_or_none(session, id=user_id)
        if not user or user.is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @classmethod
    async def update_user(cls, user_id: uuid.UUID, user: UserUpdate | UserUpdateAdmin, session: AsyncSession):
        user_update = await UserDAO.update(
            session,
            UserModel.id == user_id,
            obj_in=UserUpdateDB(
                **user.dict(exclude={"password"}),
                hashed_password=get_password_hash(user.password)
            )
        )

        if not user_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user_update

    @classmethod
    async def get_list_users(cls, offset: int, limit: int, session: AsyncSession, ):
        return await UserDAO.fild_all(session=session, offset=offset, limit=limit)

    @classmethod
    async def get_doctor(cls, id: uuid.UUID, session: AsyncSession):
        doctor = await UserDAO.find_one_or_none(session, UserModel.id == id)

        if doctor is None or 'Doctor' not in [role.name for role in doctor.roles]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

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
