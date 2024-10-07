import json

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8081/api/Authentication/SignIn")


async def validate_token(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                'http://localhost:8081/api/Authentication/Validate',
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return token
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(json.loads(exc.response.text).get('detail')))


async def get_current_user(token: str = Depends(validate_token)):
    decoded = jwt.decode(
        token, options={"verify_signature": False}
    )
    return {'token': token, 'decoded': decoded}


async def get_current_admin(user_info: dict = Depends(get_current_user)):
    if "Admin" not in user_info.get('decoded').get('roles'):
        raise HTTPException(status_code=403, detail="Not enough privileges.")
    return user_info


def validate_user_role(allowed_roles: list):
    async def role_dependency(user_info: dict = Depends(get_current_user)):
        if not any(role in allowed_roles for role in user_info.get('decoded').get('roles')):
            raise HTTPException(status_code=403, detail="Not enough privileges.")
        return user_info
    return role_dependency



