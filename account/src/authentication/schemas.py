import uuid
from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field


class CredentialsJSON(BaseModel):
    username: str
    password: str


class CredentialsFormData(BaseModel):
    username: str = Form(...)
    password: str = Form(...)


class Token(BaseModel):
    access_token: str
    refresh_token: uuid.UUID
    token_type: str


class RefreshSessionCreate(BaseModel):
    refresh_token: uuid.UUID
    access_token: str
    expires_in: int
    user_id: uuid.UUID


class RefreshSessionUpdate(RefreshSessionCreate):
    user_id: Optional[uuid.UUID] = Field(None)


class Refresh(BaseModel):
    refreshToken: uuid.UUID


