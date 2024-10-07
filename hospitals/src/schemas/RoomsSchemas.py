import uuid
from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True
