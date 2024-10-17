from fastapi import APIRouter
from src.timetable.router import router as router_timetable
from src.appointment.router import router as router_appointment


# prefix /api
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
