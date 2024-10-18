import uuid

from src.config import settings
from src.rabbitMq import RabbitMQBaseClient


class RabbitMQClient(RabbitMQBaseClient):
    def __init__(self, rabbitmq_url=f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'):
        super().__init__(rabbitmq_url)

    async def call(self, pacient_id: uuid.UUID):
        await self.connect()
        async with self.connection:
            channel, callback_queue = await self.create_channel_and_queue()
            correlation_id = str(uuid.uuid4())

            body = str(pacient_id).encode()

            await self._publish_message(
                channel=channel,
                body=body,
                routing_key='check_pacient',
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            )
            response = await self._wait_for_response(callback_queue, correlation_id)
        await self.close()
        print(response)
        return response == b'\01'
