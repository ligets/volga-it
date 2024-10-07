import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.daos.UserDAO import UserDAO
from src.database import db
from src.dependencies import get_current_user, get_current_admin
from src.models.UserModel import UserModel
from src.schemas.UserSchemas import UserDb, UserUpdate, UserCreateAdmin, UserUpdateAdmin
from src.services.UserService import UserService

router = APIRouter()


@router.get("/Me", response_model=UserDb)
async def get_user_info(
        user: UserModel = Depends(get_current_user)
):
    return user


@router.put("/Update", response_model=UserDb)
async def update_user_info(
        data: UserUpdate,
        user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await UserService.update_user(user.id, data, session)


@router.get("", response_model=list[UserDb])
async def get_list_users_info(
        offset: int = Query(..., alias="from"),
        count: int = Query(...),
        admin: UserModel = Depends(get_current_admin),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await UserService.get_list_users(offset=offset, limit=count, session=session)


@router.post("", response_model=UserDb)
async def create_user(
        data: UserCreateAdmin,
        admin: UserModel = Depends(get_current_admin),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await UserService.create_user(data, session)


@router.put("/{id}", response_model=UserDb)
async def update_user_by_id(
        id: uuid.UUID,
        data: UserUpdateAdmin,
        admin: UserModel = Depends(get_current_admin),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await UserService.update_user(id, data, session)


@router.delete("/{id}")
async def delete_user_by_id(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        admin: UserModel = Depends(get_current_admin),
):
    await UserDAO.delete(session, UserModel.id == id)

