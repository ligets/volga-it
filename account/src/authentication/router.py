from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import validate_token, get_current_user
from src.accounts.schemas import UserCreate
from src.authentication.schemas import Token, CredentialsJSON, CredentialsFormData, Refresh
from src.authentication.service import AuthService
from src.exceptions import ErrorResponseModel
from src import responses

router = APIRouter()


@router.post("/SignUp", responses={
    409: responses.username_409
})
async def sign_up(
        data: UserCreate,
        session: AsyncSession = Depends(db.get_async_session)
) -> Token:
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
    },
    'responses': {
        401: {'description': 'Invalid credentials',  'content': {'application/json': {'schema': ErrorResponseModel.model_json_schema(),'example': {'detail': 'Invalid username or password.'}}}}
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


@router.put("/SignOut", responses={
    200: {'description': 'Successful Response', 'content': None},
    401: responses.full_401,
})
async def sign_out(
        token: str = Depends(validate_token),
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.sign_out(access_token=token, session=session)


@router.get("/Validate", responses={
    200: {'description': 'Successful Response', 'content': None},
    401: responses.tokens_401
})
async def validate(accessToken: str) -> None:
    await AuthService.check_valid_token(accessToken)


@router.post("/Refresh", responses={
    401: responses.tokens_401
})
async def refresh(
        data: Refresh,
        session: AsyncSession = Depends(db.get_async_session)
):
    return await AuthService.refresh_tokens(token=data.refreshToken, session=session)
