import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class CreateAppointments(BaseModel):
    time: datetime

    @field_validator('time')
    @classmethod
    def check_time(cls, v):
        if v <= datetime.now(timezone.utc):
            raise ValueError('Время должно быть больше текущего времени')
        if v.minute % 30 != 0 or v.second != 0:
            raise ValueError('Минуты должны быть кратны 30 минутам, а секунды всегда равны 0')
        return v


class CreateAppointmentsDB(BaseModel):
    timetable_id: uuid.UUID
    time: datetime

