from typing import Generic, TypeVar, Optional, Union, Dict, Any

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions.database import DatabaseException, UnknownDatabaseException
from src.base_model import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ) -> Optional[ModelType]:
        stmt = select(cls.model).filter(*filters).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(
            cls,
            session: AsyncSession,
            *filters,
            offset: int = 0,
            limit: int = 100,
            **filter_by
    ):
        stmt = (
            select(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            obj_in: Union[CreateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        try:
            stmt = insert(cls.model).values(**create_data).returning(cls.model)
            result = await session.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError:
            raise DatabaseException
        except Exception:
            raise UnknownDatabaseException

    @classmethod
    async def delete(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ) -> None:
        stmt = delete(cls.model).filter(*filters).filter_by(**filter_by)
        await session.execute(stmt)

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        stmt = update(cls.model).where(*where).values(**update_data).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def count(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ):
        stmt = select(func.count()).select_from(cls.model).filter(*filters).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.scalar()


