import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import es
from src.dependencies import validate_pacient, validate_room_hospital, validate_doctor
from src.history.dao import HistoryDAO
from src.history.models import HistoryModel
from src.history.schemas import History


class HistoryService:
    @classmethod
    async def create_history(cls, history: History, session: AsyncSession):
        await validate_pacient(history.pacientId)
        await validate_doctor(history.doctorId)
        await validate_room_hospital(history.hospitalId, history.room)

        res: HistoryModel = await HistoryDAO.add(session, history)
        history_dict = {key: value for key, value in res.__dict__.items() if not key.startswith('_sa')}
        await es.index(index="history", id=res.id, body=history_dict)
        return res

    @classmethod
    async def get_history(cls, history_id: uuid.UUID, current_user: dict):
        res = await es.get(index="history", id=history_id)
        history = res["_source"]
        if history["pacientId"] != current_user.get('sub') and 'Doctor' not in current_user.get('roles'):
            raise HTTPException(status_code=403, detail='You are not authorized to view this history.')
        return history

    @classmethod
    async def get_history_user(cls, pacient_id: uuid.UUID, current_user: dict):
        if str(pacient_id) != current_user.get('sub') and 'Doctor' not in current_user.get('roles'):
            raise HTTPException(status_code=403, detail='You are not authorized to view this history.')

        res = await es.search(index="history", body={
            'query': {
                'term': {
                    'pacientId': pacient_id
                }
            }
        })
        return [item['_source'] for item in res['hits']['hits']]

    @classmethod
    async def update_history(cls, history_id: uuid.UUID, history: History, session: AsyncSession):
        await validate_pacient(history.pacientId)
        await validate_doctor(history.doctorId)
        await validate_room_hospital(history.hospitalId, history.room)

        res: HistoryModel = await HistoryDAO.update(session, HistoryModel.id == history_id, obj_in=history)
        if not res:
            raise HTTPException(status_code=404, detail='History not found.')
        history_dict = {key: value for key, value in res.__dict__.items() if not key.startswith('_sa')}
        await es.index(index="history", id=res.id, body=history_dict)
        return res
