import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.dependencies import validate_user_role, get_current_user
from src.appointment.schemas import CreateAppointments
from src.timetable.schemas import TimetableCreate, TimetableResponse
from src.appointment.service import AppointmentsService
from src.timetable.service import TimetableService
from fastapi_cache.decorator import cache

router = APIRouter()


@router.post('', response_model=TimetableResponse)
async def create_timetable(
        timetable: TimetableCreate,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(validate_user_role(['Admin', 'Manager']))
):
    return await TimetableService.create_timetable(timetable, session)


@router.put('/{id}', response_model=TimetableResponse)
async def update_timetable(
        id: uuid.UUID,
        timetable: TimetableCreate,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(validate_user_role(['Admin', 'Manager']))
):

    return await TimetableService.update_timetable(id, timetable, session)


@router.delete('/{id}')
async def delete_timetable(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(validate_user_role(['Admin', 'Manager']))
):
    return await TimetableService.delete_timetable(id, session)


@router.delete('/Doctor/{id}')
async def delete_doctor_timetable(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(validate_user_role(['Admin', 'Manager']))
):
    return await TimetableService.delete_doctor_timetable(id, session)


@router.delete('/Hospital/{id}')
async def delete_hospital_timetable(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(validate_user_role(['Admin', 'Manager']))
):
    return await TimetableService.delete_hospital_timetable(id, session)


@router.get('/Hospital/{id}', response_model=list[TimetableResponse])
@cache(expire=30)
async def get_hospital_timetable(
        id: uuid.UUID,
        from_datetime: datetime = Query(..., alias="from"),
        to: datetime = Query(...),
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(get_current_user)
):
    return await TimetableService.get_hospital_timetable(id, from_datetime, to, session)


@router.get('/Doctor/{id}', response_model=list[TimetableResponse])
@cache(expire=30)
async def get_doctor_timetable(
        id: uuid.UUID,
        from_datetime: datetime = Query(..., alias="from"),
        to: datetime = Query(...),
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(get_current_user)
):
    return await TimetableService.get_doctor_timetable(id, from_datetime, to, session)


@router.get('/Hospital/{id}/Room/{room}', response_model=list[TimetableResponse])
@cache(expire=30)
async def get_hospital_room_timetable(
        id: uuid.UUID,
        room: str,
        from_datetime: datetime = Query(..., alias="from"),
        to: datetime = Query(...),
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(validate_user_role(['Admin', 'Manager']))
):
    return await TimetableService.get_hospital_room_timetable(
        id, room, from_datetime, to, session
    )


@router.get('/{id}/Appointment', response_model=list[datetime])
async def get_appointment_talons(
        id: uuid.UUID,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(get_current_user)
):
    return await TimetableService.get_talons(id, session)


@router.post('/{id}/Appointment')
async def booking_appointment(
        id: uuid.UUID,
        appointment: CreateAppointments,
        session: AsyncSession = Depends(db.get_async_session),
        user: dict = Depends(get_current_user)
):
    return await AppointmentsService.booking_appointment(user, id, appointment, session)
