import uuid
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import db
from src.exceptions.AuthExceptions import InvalidToken, TokenExpiredException
from src.models.UserModel import UserModel
from src.services.UserService import UserService


oauth2 = OAuth2PasswordBearer(tokenUrl='/api/Authentication/SignIn')


async def validate_token(token: str = Depends(oauth2)):
    try:
        jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            algorithms=settings.auth_jwt.algorithm
        )
        return token
    except ExpiredSignatureError:
        raise TokenExpiredException
    except Exception:
        raise InvalidToken


async def get_current_user(token: str = Depends(oauth2), session: AsyncSession = Depends(db.get_async_session)) -> Optional[any]:
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            algorithms=settings.auth_jwt.algorithm
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidToken
    except ExpiredSignatureError:
        raise TokenExpiredException
    except Exception:
        raise InvalidToken

    current_user: UserModel = await UserService.get_user(uuid.UUID(user_id), session)
    return current_user


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


