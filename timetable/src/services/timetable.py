from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from src.daos.timetable import TimetableDAO
from src.schemas.timetable import TimetableCreate
import json


class TimetableService:

    @classmethod
    async def create_timetable(cls, timetable: TimetableCreate, session: AsyncSession, token: str):
        async with httpx.AsyncClient() as client:
            try:
                doc_response = await client.get(
                    f'http://localhost:8081/api/Doctors/{timetable.doctorId}',
                    headers={"Authorization": f"Bearer {token}"},
                )
                doc_response.raise_for_status()

                hospital_response = await client.get(
                    f'http://localhost:8082/api/Hospitals/{timetable.hospitalId}/Rooms',
                    headers={"Authorization": f"Bearer {token}"},
                )
                hospital_response.raise_for_status()
                rooms = hospital_response.json()

                room = next((room.get('name') for room in rooms if room.get('name') == timetable.room), None)
                if not room:
                    raise HTTPException(status_code=404, detail='Room not found.')

                return await TimetableDAO.add(session, timetable)

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=json.loads(exc.response.text).get('detail')
                )


