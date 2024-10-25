from typing import Union, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.base_dao import BaseDAO
from src.exceptions.database import DatabaseException, ConflictUniqueAttribute, UnknownDatabaseException
from .models import HospitalModel
from .models import RoomModel
from .schemas import HospitalCreateDB, HospitalUpdateDB


class HospitalsDAO(BaseDAO[HospitalModel, HospitalCreateDB, HospitalUpdateDB]):
    model = HospitalModel

    @classmethod
    async def get_rooms(cls, session: AsyncSession, *filters, **filter_by):
        stmt = select(cls.model).options(selectinload(cls.model.rooms)).filter(*filters).filter_by(**filter_by)
        result = await session.execute(stmt)
        hospital = result.scalars().one_or_none()

        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hospital not found.')

        return hospital.rooms

    @classmethod
    async def update_rooms(cls, session: AsyncSession, rooms, hospital: HospitalModel):
        existing_rooms_stmt = select(RoomModel).where(RoomModel.name.in_(rooms))
        result = await session.execute(existing_rooms_stmt)
        existing_rooms = result.scalars().all()

        # Определяем, какие комнаты уже существуют, а какие нужно создать
        new_room_names = set(rooms) - {room.name for room in existing_rooms}

        # Добавляем новые комнаты
        if new_room_names:
            new_rooms_stmt = (insert(RoomModel).values([{"name": name} for name in new_room_names])
                              .returning(RoomModel))
            result = await session.execute(new_rooms_stmt)
            new_rooms = result.scalars().all()
            all_rooms = existing_rooms + new_rooms
        else:
            all_rooms = existing_rooms

        # Связываем комнаты с больницей
        hospital.rooms = all_rooms

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in: Union[HospitalUpdateDB, Dict[str, Any]],
    ) -> Optional[HospitalModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        rooms = update_data.pop('rooms', None)
        try:
            stmt = update(cls.model) \
                .where(*where) \
                .values(**update_data) \
                .returning(cls.model) \
                .options(selectinload(cls.model.rooms))
            result = await session.execute(stmt)
            hospital: HospitalModel = result.scalars().one_or_none()
            if rooms and hospital:
                await cls.update_rooms(session, rooms, hospital)
            return hospital
        except SQLAlchemyError:
            raise DatabaseException
        except Exception:
            raise UnknownDatabaseException

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            obj_in: Union[HospitalCreateDB, Dict[str, Any]],
    ):
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        rooms = create_data.pop('rooms', None)

        try:
            stmt = insert(cls.model).values(**create_data).returning(cls.model).options(selectinload(cls.model.rooms))
            result = await session.execute(stmt)
            hospital: HospitalModel = result.scalars().first()
            if rooms:
                await cls.update_rooms(session, rooms, hospital)
            return hospital
        except SQLAlchemyError:
            raise DatabaseException
        except Exception:
            raise UnknownDatabaseException
