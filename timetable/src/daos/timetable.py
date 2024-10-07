from . import BaseDAO
from src.models.timetable import TimetableModel
from src.schemas.timetable import TimetableCreate


class TimetableDAO(BaseDAO[TimetableModel, TimetableCreate, TimetableCreate]):
    model = TimetableModel
