import uuid

from src.config import settings
from . import RabbitMQBaseClient


class RabbitMQClient(RabbitMQBaseClient):
    def __init__(self, rabbitmq_url=f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'):
        super().__init__(rabbitmq_url)

    async def call(self, hospital_id: uuid.UUID):
        await self.connect()
        async with self.connection:
            channel = await self.connection.channel()

            body = str(hospital_id).encode()

            await self._publish_message(
                channel=channel,
                body=body,
                routing_key='delete_timetable_hospital'
            )

        await self.close()

