import time
import uuid
from functools import partial
import aio_pika
from fastapi import HTTPException
from sqlalchemy import and_

from src.config import settings
from src.accounts.dao import UserDAO
from src.database import db
from src.accounts.models import UserModel
from src.dependencies import validate_token
from src.doctors.service import DoctorService
from src.exceptions.AuthExceptions import TokenExpiredException, InvalidToken


async def check_doctor(message: aio_pika.abc.AbstractIncomingMessage, channel: aio_pika.RobustChannel):
    async with message.process():
        doctor_id = message.body.decode()
        try:
            async with db.session() as session:
                doctor = await DoctorService.get_doctor(uuid.UUID(doctor_id), session)
                response = b'\x01'
        except HTTPException:
            response = b'\x00'
        if message.reply_to:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def check_token(message: aio_pika.abc.AbstractIncomingMessage, channel: aio_pika.RobustChannel):
    async with message.process():
        token = message.body.decode()
        try:
            await validate_token(token=token)
            response = b'\x01'
        except HTTPException as e:
            response = str(e.detail).encode()

        if message.reply_to:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def consume_rabbitmq():
    connection = await aio_pika.connect_robust(
        f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'
    )
    channel = await connection.channel()

    doctor_queue = await channel.declare_queue(
        'check_doctor', auto_delete=True
    )
    await doctor_queue.consume(partial(check_doctor, channel=channel))

    token_queue = await channel.declare_queue(
        'check_token', auto_delete=True
    )
    await token_queue.consume(partial(check_token, channel=channel))
