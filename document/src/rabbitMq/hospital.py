import json
import uuid
from . import RabbitMQBaseClient
from ..config import settings


class RabbitMQClient(RabbitMQBaseClient):
    def __init__(self, rabbitmq_url=f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'):
        super().__init__(rabbitmq_url)

    async def call_room(self, hospital_id: uuid.UUID, room: str):
        await self.connect()
        async with self.connection:
            channel, callback_queue = await self.create_channel_and_queue()
            correlation_id = str(uuid.uuid4())

            body = json.dumps({
                'hospital_id': str(hospital_id),
                'room': room
            }).encode()

            await self._publish_message(
                channel=channel,
                body=body,
                routing_key='check_hospital_room',
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            )

            response = await self._wait_for_response(callback_queue, correlation_id)
        await self.close()
        if response == b'\x01':
            return True
        return response.decode()

    async def call_hospital(self, hospital_id: uuid.UUID):
        await self.connect()
        async with self.connection:
            channel, callback_queue = await self.create_channel_and_queue()
            correlation_id = str(uuid.uuid4())

            body = str(hospital_id).encode()

            await self._publish_message(
                channel=channel,
                body=body,
                routing_key='check_hospital',
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            )

            response = await self._wait_for_response(callback_queue, correlation_id)
        await self.close()
        return response == b'\x01'

