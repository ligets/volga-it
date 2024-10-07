import uuid

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import validate_token
from src.exceptions.AuthExceptions import InvalidToken
from src.schemas.UserSchemas import UserCreate
from src.schemas.AuthSchemas import Token
from src.services.AuthService import AuthService

router = APIRouter()


@router.post("/SignUp")
async def sign_up(
        data: UserCreate,
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.sign_up(data, session)


@router.post("/SignIn")
async def sign_in(
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(db.get_async_session)
) -> Token:
    return await AuthService.sign_in(credentials.username, credentials.password, session)


@router.put("/SignOut")
async def sign_out(
        token: str = Depends(validate_token),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.sign_out(access_token=token, session=session)


@router.get("/Validate")
async def validate_token(
        token: str = Depends(validate_token)
):
    return {"valid": True} if token else InvalidToken


@router.post("/Refresh")
async def refresh(
        refreshToken: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.refresh_tokens(token=refreshToken, session=session)

