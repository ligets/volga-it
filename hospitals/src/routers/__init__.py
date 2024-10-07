from fastapi import APIRouter
from .HospitalsRouter import router as router_hospitals


all_routers = APIRouter()

all_routers.include_router(
    router_hospitals,
    prefix='/Hospitals',
    tags=['Hospitals']
)

