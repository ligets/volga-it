import uuid
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import db
from src.exceptions.AuthExceptions import InvalidToken, TokenExpiredException
from src.accounts.models import UserModel
from src.rabbitMq.timetable import RabbitMQClient


oauth2 = OAuth2PasswordBearer(tokenUrl='/api/Authentication/SignIn')


async def validate_token(token: str = Depends(oauth2)):
    try:
        decode = jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )
        if decode.get('is_deleted') is True:
            raise InvalidToken
        return token
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except jwt.PyJWTError:
        raise InvalidToken


async def get_current_user(token: str = Depends(oauth2), session: AsyncSession = Depends(db.get_async_session)) -> Optional[any]:
    from src.accounts.service import UserService
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )
        user_id = payload.get("sub")
        if user_id is None or payload.get('is_deleted') is True:
            raise InvalidToken
        current_user: UserModel = await UserService.get_user(user_id, session)
        return current_user
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except (jwt.PyJWTError, HTTPException):
        raise InvalidToken


async def get_current_manager(current_user: UserModel = Depends(get_current_user)):
    if 'Manager' not in [role.name for role in current_user.roles]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges.")
    return current_user


async def get_current_doctor(current_user: UserModel = Depends(get_current_user)):
    if 'Doctor' not in [role.name for role in current_user.roles]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges.")
    return current_user


async def get_current_admin(current_user: UserModel = Depends(get_current_user)):
    if 'Admin' not in [role.name for role in current_user.roles]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges.")
    return current_user


async def delete_timetable_doctor(doctor_id: uuid.UUID):
    rabbitmq = RabbitMQClient()
    await rabbitmq.call(doctor_id)

