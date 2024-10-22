import uuid
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field, field_validator, ConfigDict


class TimetableCreate(BaseModel):
    hospitalId: uuid.UUID
    doctorId: uuid.UUID
    from_column: datetime = Field(..., alias='from')
    to: datetime = Field(..., alias='to')
    room: str

    @field_validator('from_column', 'to')
    @classmethod
    def check_date_format(cls, v):
        if v.minute % 30 != 0 or v.second != 0:
            raise ValueError('Минуты должны быть кратны 30 минутам, а секунды всегда равны 0')
        current_time = datetime.now(timezone.utc)
        if v <= current_time:
            raise ValueError("Время должно быть больше текущего")
        return v

    @field_validator('to')
    @classmethod
    def check_time_order(cls, to_time, values):
        from_time = values.data.get('from_time')
        if from_time and to_time <= from_time:
            raise ValueError("Поле 'to' должно быть больше, чем 'from'")
        return to_time

    @field_validator('to')
    @classmethod
    def check_time_difference(cls, to_time, values):
        from_time = values.data.get('from_time')
        if from_time and (to_time - from_time) > timedelta(hours=12):
            raise ValueError('Разница между временем начала и конца должна быть не менее 30 минут')
        return to_time


class TimetableResponse(BaseModel):
    id: uuid.UUID
    hospitalId: uuid.UUID
    doctorId: uuid.UUID
    from_column: datetime
    to: datetime
    room: str

    model_config = ConfigDict(from_attributes=True)


