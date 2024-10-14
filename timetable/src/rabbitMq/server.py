import uuid

import aio_pika

from src.config import settings
from src.database import db
from src.services.timetable import TimetableService


async def delete_doctor(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        doctor_id = message.body.decode()
        async with db.session() as session:
            await TimetableService.delete_doctor_timetable(uuid.UUID(doctor_id), session)
            await session.commit()


async def delete_hospital(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        hospital_id = message.body.decode()
        async with db.session() as session:
            await TimetableService.delete_hospital_timetable(uuid.UUID(hospital_id), session)
            await session.commit()


async def consume_rabbitmq():
    connection = await aio_pika.connect_robust(
        f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'
    )
    channel = await connection.channel()

    hospital_room_queue = await channel.declare_queue(
        'delete_timetable_doctor', auto_delete=True
    )
    await hospital_room_queue.consume(delete_doctor)

    hospital_queue = await channel.declare_queue(
        'delete_timetable_hospital', auto_delete=True
    )
    await hospital_queue.consume(delete_hospital)