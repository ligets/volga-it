from typing import List, Optional
import uuid
from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class HospitalBase(BaseModel):
    name: str
    address: str
    contactPhone: str


class HospitalCreate(HospitalBase):
    rooms: List[str]


class HospitalCreateDB(HospitalCreate):
    rooms: Optional[List[str]] = None


class HospitalUpdate(HospitalBase):
    rooms: List[str]


class HospitalUpdateDB(HospitalBase):
    rooms: Optional[List[str]] = None


class HospitalResponse(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    contactPhone: str

    class Config:
        from_attributes = True


class HospitalCreateResponse(HospitalResponse):
    rooms: List[RoomResponse]



