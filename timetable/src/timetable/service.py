from datetime import datetime, timedelta, timezone
import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from src.timetable.dao import TimetableDAO
from src.dependencies import validate_doctor, validate_room_hospital, validate_hospital
from src.timetable.model import TimetableModel
from src.timetable.schemas import TimetableCreate


class TimetableService:

    @classmethod
    async def create_timetable(cls, timetable: TimetableCreate, session: AsyncSession):
        await validate_doctor(timetable.doctorId)
        await validate_room_hospital(timetable.hospitalId, timetable.room)

        return await TimetableDAO.add(session, timetable)

    @classmethod
    async def update_timetable(cls, timetable_id: uuid.UUID, timetable: TimetableCreate, session: AsyncSession):
        await validate_doctor(timetable.doctorId)
        await validate_room_hospital(timetable.hospitalId, timetable.room)
        timetable_db = await TimetableDAO.find_one_or_none(session, TimetableModel.id == timetable_id)
        if not timetable_db:
            raise HTTPException(status_code=404, detail='Timetable not found')
        if timetable_db.appointments:
            raise HTTPException(status_code=409, detail='Timetable already has appointments')
        return await TimetableDAO.update(session, TimetableModel.id == timetable_id, obj_in=timetable)

    @classmethod
    async def delete_timetable(cls, timetable_id: uuid.UUID, session: AsyncSession):
        await TimetableDAO.delete(session, TimetableModel.id == timetable_id)

    @classmethod
    async def delete_doctor_timetable(cls, doctor_id: uuid.UUID, session: AsyncSession):
        await TimetableDAO.delete(session, TimetableModel.doctorId == doctor_id)

    @classmethod
    async def delete_hospital_timetable(cls, hospital_id: uuid.UUID, session: AsyncSession):
        await TimetableDAO.delete(session, TimetableModel.hospitalId == hospital_id)

    @classmethod
    async def get_hospital_timetable(
            cls,
            hospital_id: uuid.UUID,
            from_datetime: datetime,
            to: datetime,
            session: AsyncSession
    ):
        if from_datetime >= to:
            raise HTTPException(status_code=422, detail=[
                {
                    'loc': ['query', 'to'],
                    'msg': "Поле 'to' должно быть больше, чем 'from'"
                }
            ])
        await validate_hospital(hospital_id)
        if to.time() == datetime.min.time():
            to += timedelta(days=1)
        return await TimetableDAO.fild_all(
            session,
            and_(
                TimetableModel.hospitalId == hospital_id,
                TimetableModel.to > from_datetime,
                TimetableModel.from_column < to
            )
        )

    @classmethod
    async def get_doctor_timetable(
            cls,
            doctor_id: uuid.UUID,
            from_datetime: datetime,
            to: datetime,
            session: AsyncSession
    ):
        if from_datetime >= to:
            raise HTTPException(status_code=422, detail=[
                {
                    'loc': ['query', 'to'],
                    'msg': "Поле 'to' должно быть больше, чем 'from'"
                }
            ])
        await validate_doctor(doctor_id)
        if to.time() == datetime.min.time():
            to += timedelta(days=1)
        return await TimetableDAO.fild_all(
            session,
            and_(
                TimetableModel.doctorId == doctor_id,
                TimetableModel.to > from_datetime,
                TimetableModel.from_column < to
            )
        )

    @classmethod
    async def get_hospital_room_timetable(
            cls,
            hospital_id: uuid.UUID,
            room: str,
            from_datetime: datetime,
            to: datetime,
            session: AsyncSession
    ):
        if from_datetime >= to:
            raise HTTPException(status_code=422, detail=[
                {
                    'loc': ['query', 'to'],
                    'msg': "Поле 'to' должно быть больше, чем 'from'"
                }
            ])
        await validate_room_hospital(hospital_id, room)
        if to.time() == datetime.min.time():
            to += timedelta(days=1)
        return await TimetableDAO.fild_all(
            session,
            and_(
                TimetableModel.hospitalId == hospital_id,
                TimetableModel.room == room,
                TimetableModel.to > from_datetime,
                TimetableModel.from_column < to
            )
        )

    @classmethod
    async def get_talons(
            cls,
            timetable_id: uuid.UUID,
            session: AsyncSession
    ):
        timetable = await TimetableDAO.find_one_or_none(session, TimetableModel.id == timetable_id)
        if not timetable:
            raise HTTPException(status_code=404, detail='Timetable not found.')
        current_datetime = datetime.now(tz=timezone.utc)
        talons = []
        start_time = timetable.from_column
        end_time = timetable.to
        if end_time < current_datetime:
            raise HTTPException(status_code=400, detail='Timetable is already passed.')

        lock_appointments = {appoint.time for appoint in timetable.appointments}

        while start_time < end_time:
            if start_time in lock_appointments or start_time < current_datetime:
                start_time += timedelta(minutes=30)
                continue
            talons.append(start_time)
            start_time += timedelta(minutes=30)

        return talons

