import uuid
from datetime import timedelta, datetime, timezone

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.accounts.dao import UserDAO
from src.authentication.dao import RefreshSessionDAO
from src.exceptions.AuthExceptions import InvalidToken, TokenExpiredException, InvalidCredentialsException
from src.accounts.models import UserModel
from src.authentication.models import RefreshSessionModel
from src.authentication.schemas import Token, RefreshSessionCreate, RefreshSessionUpdate
from src.accounts.schemas import UserCreate
from src.accounts.service import UserService
from src.authentication.utils import is_valid_password


class AuthService:
    @classmethod
    async def sign_up(cls, data: UserCreate, session):
        user = await UserService.create_user(data, session)
        return await cls.create_token(user, session)

    @classmethod
    async def sign_in(cls, username: str, password: str, session: AsyncSession) -> Token:
        user: UserModel = await UserDAO.find_one_or_none(session, username=username)
        if user and not user.is_deleted and is_valid_password(password, user.hashed_password):
            return await cls.create_token(user, session)
        raise InvalidCredentialsException

    @classmethod
    async def sign_out(cls, access_token: str, session: AsyncSession):
        await RefreshSessionDAO.delete(session, RefreshSessionModel.access_token == access_token)

    @classmethod
    async def refresh_tokens(cls, session: AsyncSession, token: uuid.UUID):
        refresh_session: RefreshSessionModel = await RefreshSessionDAO.find_one_or_none(
            session,
            RefreshSessionModel.refresh_token == token
        )
        if refresh_session is None:
            raise InvalidToken
        if datetime.now(timezone.utc) >= refresh_session.created_at + timedelta(seconds=refresh_session.expires_in):
            await RefreshSessionDAO.delete(session, RefreshSessionModel.refresh_token == token)
            raise TokenExpiredException
        user = await UserDAO.find_one_or_none(session, UserModel.id == refresh_session.user_id)
        if not user or user.is_deleted:
            raise InvalidToken
        access_token = await cls._create_access_token(user)
        refresh_token = await cls._create_refresh_token()
        refresh_token_expires = timedelta(
            days=settings.auth_jwt.refresh_token_expire_days
        )
        await RefreshSessionDAO.update(
            session,
            RefreshSessionModel.refresh_token == refresh_session.refresh_token,
            obj_in=RefreshSessionUpdate(
                refresh_token=refresh_token,
                access_token=access_token,
                expires_in=refresh_token_expires.total_seconds()
            )
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type='Bearer')

    @classmethod
    async def create_token(cls, user: UserModel, session: AsyncSession) -> Token:
        access_token = await cls._create_access_token(user)
        refresh_token_expires = timedelta(
            days=settings.auth_jwt.refresh_token_expire_days
        )
        refresh_token = await cls._create_refresh_token()

        await RefreshSessionDAO.add(
            session,
            RefreshSessionCreate(
                user_id=user.id,
                refresh_token=refresh_token,
                access_token=access_token,
                expires_in=refresh_token_expires.total_seconds()
            )
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type='Bearer')

    @classmethod
    async def abort_all_sessions(cls, user_id: uuid.UUID, session: AsyncSession, ):
        await RefreshSessionDAO.delete(session, RefreshSessionModel.user_id == user_id)

    @classmethod
    async def _create_access_token(cls, user: UserModel) -> str:
        to_encode = {
            'sub': str(user.id),
            'firsName': user.firstName,
            'lastName': user.lastName,
            'roles': [role.name for role in user.roles],
            'is_deleted': user.is_deleted,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.auth_jwt.private_key_path.read_text(),
            algorithm=settings.auth_jwt.algorithm
        )
        return encoded_jwt

    @classmethod
    async def _create_refresh_token(cls) -> str:
        return str(uuid.uuid4())

