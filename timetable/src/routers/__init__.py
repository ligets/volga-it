from fastapi import APIRouter
from .timetable import router as router_timetable
from .appointment import router as router_appointment


all_routers = APIRouter()

all_routers.include_router(
    router_timetable,
    prefix='/Timetable',
    tags=['Timetable'],
)

all_routers.include_router(
    router_appointment,
    prefix='/Appointment',
    tags=['Appointment'],
)
