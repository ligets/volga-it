import uuid
from datetime import datetime

from pydantic import BaseModel


class History(BaseModel):
    date: datetime
    pacientId: uuid.UUID
    hospitalId: uuid.UUID
    doctorId: uuid.UUID
    room: str
    data: str


class HistoryResponse(BaseModel):
    id: uuid.UUID
    date: datetime
    pacientId: uuid.UUID
    hospitalId: uuid.UUID
    doctorId: uuid.UUID
    room: str
    data: str
