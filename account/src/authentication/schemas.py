import uuid
from typing import Optional
from pydantic import BaseModel, Field


class UserAuth(BaseModel):
    username: str
    password: str


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


