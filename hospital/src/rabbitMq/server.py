import asyncio
import json
from functools import partial

import aio_pika
from fastapi import HTTPException

from src.config import settings, logger
from src.hospitals.dao import HospitalsDAO
from src.database import db
from src.hospitals.models import HospitalModel


async def check_hospital_room(message: aio_pika.abc.AbstractIncomingMessage, channel: aio_pika.RobustChannel):
    async with message.process():
        body = json.loads(message.body.decode())
        hospital_id = body.get('hospital_id')
        query_room = body.get('room')
        async with db.session() as session:
            try:
                rooms = await HospitalsDAO.get_rooms(session, HospitalModel.id == hospital_id)
                room = next((room.name for room in rooms if room.name == query_room), None)
                if room:
                    response = b'\x01'
                else:
                    response = 'Room not found.'.encode()
            except HTTPException:
                response = 'Hospital not found.'.encode()
        if message.reply_to:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def check_hospital(message: aio_pika.abc.AbstractIncomingMessage, channel: aio_pika.RobustChannel):
    async with message.process():
        hospital_id = message.body.decode()
        async with db.session() as session:
            room = await HospitalsDAO.find_one_or_none(session, HospitalModel.id == hospital_id)
            if room:
                response = b'\x01'
            else:
                response = b'\x00'
        if message.reply_to:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def consume_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust(f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/')
            channel = await connection.channel()

            hospital_room_queue = await channel.declare_queue(
                'check_hospital_room', auto_delete=True
            )
            await hospital_room_queue.consume(partial(check_hospital_room, channel=channel))

            hospital_queue = await channel.declare_queue(
                'check_hospital', auto_delete=True
            )
            await hospital_queue.consume(partial(check_hospital, channel=channel))
            logger.info('Успешное подключение к RabbitMQ')
            break

        except Exception as e:
            logger.error(f'Ошибка подключения к RabbitMQ: {e}. Переподключение через 5 секунд...')
            await asyncio.sleep(5)

