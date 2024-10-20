import uuid
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    id: int
    name: str


class UserBase(BaseModel):
    firstName: str
    lastName: str
    username: str


class UserDb(BaseModel):
    id: uuid.UUID
    firstName: str
    lastName: str
    username: str
    roles: list[RoleSchema]

    model_config = {'from_attributes': True}


class UserCreate(UserBase):
    firstName: str
    lastName: str
    username: str
    password: str


class UserCreateAdmin(UserCreate):
    roles: List[str]


class UserCreateDB(BaseModel):
    lastName: str
    firstName: str
    username: str
    hashed_password: str
    roles: Optional[List[str]] = None


class UserUpdate(BaseModel):
    firstName: str
    lastName: str
    password: str


class UserUpdateAdmin(UserUpdate):
    username: str
    roles: List[str]


class UserUpdateDB(BaseModel):
    lastName: str
    firstName: str
    username: Optional[str] = None
    hashed_password: str
    roles: Optional[List[str]] = None


class ResponseDoctor(BaseModel):
    id: uuid.UUID
    firstName: str
    lastName: str


