from typing import Optional, Union, Dict, Any

from sqlalchemy import select, insert, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.exceptions.DatabaseException import DatabaseException, UnknownDatabaseException, ConflictUniqueAttribute
from src.accounts.models import UserModel
from src.accounts.models import RoleModel
from src.accounts.schemas import UserCreateDB, UserUpdateDB
from src.base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ) -> Optional[UserModel]:
        stmt = select(cls.model).options(selectinload(cls.model.roles)).filter(*filters).filter_by(**filter_by)
        result = await session.execute(stmt)
        # print(result.all())
        return result.scalars().one_or_none()

    @classmethod
    async def fild_all(
            cls,
            session: AsyncSession,
            *filters,
            offset: int = 0,
            limit: int = 100,
            **filter_by
    ):
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.roles))
            .join(cls.model.roles)
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in: Union[UserUpdateDB, Dict[str, Any]],
    ) -> Optional[UserModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        roles = update_data.pop("roles", None)

        stmt = update(cls.model).where(*where).values(**update_data).returning(cls.model).options(selectinload(cls.model.roles))
        result = await session.execute(stmt)
        updated_user = result.scalars().one_or_none()

        if updated_user and roles is not None:
            current_roles = {role.name for role in updated_user.roles}

            new_roles_query = await session.execute(select(RoleModel).where(RoleModel.name.in_(roles)))
            new_roles = new_roles_query.scalars().all()

            # Формируем множество с именами новых ролей
            new_roles_set = {role.name for role in new_roles}

            # Добавляем новые роли, которые отсутствуют у пользователя
            roles_to_add = new_roles_set - current_roles
            for role in new_roles:
                if role.name in roles_to_add:
                    updated_user.roles.append(role)

            # Удаляем роли, которые отсутствуют в новом списке
            roles_to_remove = current_roles - new_roles_set
            updated_user.roles = [role for role in updated_user.roles if role.name not in roles_to_remove]

        return updated_user

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            obj_in: Union[UserCreateDB, Dict[str, Any]],
    ) -> Optional[UserModel]:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        roles = create_data.pop("roles", None)

        try:
            stmt = insert(cls.model).values(**create_data).returning(cls.model).options(selectinload(cls.model.roles))
            result = await session.execute(stmt)
            user: UserModel = result.scalars().first()

            if user:
                if not roles:
                    roles = ['User']

                new_roles_query = await session.execute(select(RoleModel).where(RoleModel.name.in_(roles)))
                new_roles = new_roles_query.scalars().all()
                user.roles.extend(new_roles)
                return user
        except IntegrityError:
            raise ConflictUniqueAttribute('Username is already taken.')
        except SQLAlchemyError:
            raise DatabaseException
        except Exception:
            raise UnknownDatabaseException
