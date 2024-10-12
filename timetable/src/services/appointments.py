import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.daos.appointments import AppointmentDAO
from src.daos.timetable import TimetableDAO
from src.models.timetable import TimetableModel
from src.schemas.appointments import CreateAppointments, CreateAppointmentsDB


class AppointmentsService:
    @classmethod
    async def booking_appointment(cls, timetable_id: uuid.UUID, appointment: CreateAppointments, session: AsyncSession):
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
                time=appointment.time
            )
        )


