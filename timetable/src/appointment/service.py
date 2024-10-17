import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.appointment.dao import AppointmentDAO
from src.timetable.dao import TimetableDAO
from src.timetable.model import TimetableModel
from src.appointment.schemas import CreateAppointments, CreateAppointmentsDB


class AppointmentsService:
    @classmethod
    async def booking_appointment(
            cls,
            user,
            timetable_id: uuid.UUID,
            appointment: CreateAppointments,
            session: AsyncSession
    ):
        timetable = await TimetableDAO.find_one_or_none(session, TimetableModel.id == timetable_id)
        if not timetable:
            raise HTTPException(status_code=404, detail='Timetable not found')
        if not timetable.from_column <= appointment.time < timetable.to:
            raise HTTPException(status_code=400, detail='Timetable is not available for this time')
        lock_appointments = {appoint.time for appoint in timetable.appointments}
        if appointment.time in lock_appointments:
            raise HTTPException(status_code=409, detail='Appointment already booked')

        return await AppointmentDAO.add(
            session,
            CreateAppointmentsDB(
                timetable_id=timetable.id,
                user_id=user.get('sub'),
                time=appointment.time
            )
        )

    @classmethod
    async def delete_appointment(cls, user, appointment_id: uuid.UUID, session: AsyncSession):
        appointment = await AppointmentDAO.find_one_or_none(session, id=appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail='Appointment not found')
        if appointment.user_id != user.get('sub') and not any(role in ['Admin', 'Manager'] for role in user.get('roles')):
            raise HTTPException(status_code=403, detail='You are not authorized to delete this appointment')
        if appointment.time <= datetime.datetime.now(datetime.timezone.utc):
            raise HTTPException(status_code=400, detail='Cannot delete a meeting that has started')

        await AppointmentDAO.delete(session, id=appointment_id)

