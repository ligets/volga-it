from fastapi import APIRouter
from src.history.router import router as history_router


all_routers = APIRouter()

all_routers.include_router(
    history_router,
    prefix='/History',
    tags=['History']
)
