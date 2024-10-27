from fastapi import APIRouter, Depends
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src import responses
from src.database import db
from src.dependencies import get_current_user, validate_user_role
from src.history.schemas import History, HistoryResponse
from src.history.service import HistoryService

router = APIRouter()

router.responses = {
    401: responses.full_401
}


@router.get('/Account/{id}', response_model=list[HistoryResponse], responses={
    403: responses.view_403,
    404: responses.pacient_404
})
async def get_account_history(
        id: uuid.UUID,
        current_user: dict = Depends(get_current_user)
):
    return await HistoryService.get_history_user(id, current_user)


@router.get('/{id}', response_model=HistoryResponse, responses={
    403: responses.view_403,
    404: responses.history_404
})
async def get_history(
        id: uuid.UUID,
        current_user: dict = Depends(get_current_user)
):
    return await HistoryService.get_history(id, current_user)


@router.post('', response_model=HistoryResponse, responses={
    403: responses.forb_403,
    404: responses.validate_404
})
async def create_history(
        history: History,
        session: AsyncSession = Depends(db.get_async_session),
        current_user: dict = Depends(validate_user_role(['Admin', 'Manager', 'Doctor']))
):
    return await HistoryService.create_history(history, session)


@router.put('/{id}', response_model=HistoryResponse, responses={
    403: responses.forb_403,
    404: responses.full_404
})
async def update_history(
        id: uuid.UUID,
        history: History,
        session: AsyncSession = Depends(db.get_async_session),
        current_user: dict = Depends(validate_user_role(['Admin', 'Manager', 'Doctor']))
):
    return await HistoryService.update_history(id, history, session)
