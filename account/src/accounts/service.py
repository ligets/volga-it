import uuid

from fastapi import HTTPException, status
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.dao import UserDAO
from src.dependencies import delete_timetable_doctor
from src.accounts.models import UserModel
from src.accounts.models import RoleModel
from src.accounts.schemas import UserUpdate, UserUpdateDB, UserUpdateAdmin, \
    UserCreate, UserCreateAdmin, UserCreateDB
from src.authentication.utils import get_password_hash


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
    async def get_user(cls, user_id: uuid.UUID, session: AsyncSession) -> UserModel:
        user = await UserDAO.find_one_or_none(session, id=user_id)
        if not user or user.is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @classmethod
    async def update_user(cls, user_id: uuid.UUID, user: UserUpdate | UserUpdateAdmin, session: AsyncSession):
        if isinstance(user, UserUpdateAdmin):
            current_user = await cls.get_user(user_id, session)
            if 'Doctor' in [role.name for role in current_user.roles] and 'Doctor' not in user.roles:
                await delete_timetable_doctor(current_user.id)
        user_update = await UserDAO.update(
            session,
            and_(UserModel.id == user_id, UserModel.is_deleted == False),
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
        return await UserDAO.fild_all(session, UserModel.is_deleted == False, offset=offset, limit=limit)

    @classmethod
    async def delete_user(cls, user_id: uuid.UUID, session: AsyncSession):
        user = await cls.get_user(user_id, session)
        if 'Doctor' in [role.name for role in user.roles]:
            await delete_timetable_doctor(user.id)

        await UserDAO.update(session, UserModel.id == user.id, obj_in={'is_deleted': True})
