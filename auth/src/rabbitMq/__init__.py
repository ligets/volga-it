from functools import partial
import aio_pika
from src.config import settings
from src.daos.UserDAO import UserDAO
from src.database import db
from src.models.UserModel import UserModel


async def on_request(message: aio_pika.abc.AbstractIncomingMessage, channel: aio_pika.RobustChannel):
    async with message.process():
        doctor_id = message.body.decode()
        async with db.session() as session:
            doctor = await UserDAO.find_one_or_none(session, UserModel.id == doctor_id)
            if not doctor or 'Doctor' not in [role.name for role in doctor.roles]:
                response = b'\x00'
            else:
                response = b'\x01'
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

    queue = await channel.declare_queue(
        'check_doctor', auto_delete=True
    )
    await queue.consume(partial(on_request, channel=channel))
