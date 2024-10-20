import uuid

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import validate_token, get_current_user
from src.exceptions.AuthExceptions import InvalidToken
from src.accounts.schemas import UserCreate
from src.authentication.schemas import Token, CredentialsJSON, CredentialsFormData, Refresh
from src.authentication.service import AuthService

router = APIRouter()


@router.post("/SignUp")
async def sign_up(
        data: UserCreate,
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.sign_up(data, session)


@router.post("/SignIn", openapi_extra={
    'requestBody': {
        'content': {
            'application/json': {
               'schema': CredentialsJSON.model_json_schema()
            },
            'application/x-www-form-urlencoded': {
               'schema': CredentialsFormData.model_json_schema()
            }
        },
        'required': True
    }
})
async def sign_in(
        request: Request,
        session: AsyncSession = Depends(db.get_async_session)
) -> Token:
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        credentials = await request.json()
        credentials_model = CredentialsJSON(**credentials)
    elif content_type == "application/x-www-form-urlencoded":
        form = await request.form()
        credentials_model = CredentialsJSON(username=form["username"], password=form["password"])
    else:
        raise HTTPException(status_code=415, detail="Unsupported media type")
    return await AuthService.sign_in(credentials_model.username, credentials_model.password, session)


@router.put("/SignOut")
async def sign_out(
        token: str = Depends(validate_token),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.sign_out(access_token=token, session=session)


@router.get("/Validate")
async def validate_token(
        user: str = Depends(get_current_user)
):
    pass


@router.post("/Refresh")
async def refresh(
        data: Refresh,
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.refresh_tokens(token=data.refreshToken, session=session)

