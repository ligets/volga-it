import asyncio
import json
import uuid
import aio_pika
from fastapi import HTTPException
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

    # async def call_hospital(self, hospital_id: uuid.UUID):
    #     connection = await aio_pika.connect_robust(self.rabbitmq_url)
    #     async with connection:
    #         channel = await connection.channel()
    #         callback_queue = await channel.declare_queue(auto_delete=True)
    #
    #         correlation_id = str(uuid.uuid4())
    #
    #         loop = asyncio.get_running_loop()
    #         future_response = loop.create_future()
    #
    #         async def on_response(msg: aio_pika.abc.AbstractIncomingMessage):
    #             async with msg.process():
    #                 if msg.correlation_id == correlation_id:
    #                     future_response.set_result(msg.body == b'\x01')
    #
    #         await callback_queue.consume(
    #             on_response
    #         )
    #         try:
    #             await channel.default_exchange.publish(
    #                 aio_pika.Message(
    #                     body=json.dumps({
    #                         'hospital_id': str(hospital_id),
    #                     }).encode(),
    #                     correlation_id=correlation_id,
    #                     reply_to=callback_queue.name,
    #                 ),
    #                 routing_key='check_hospital'
    #             )
    #
    #             response = await asyncio.wait_for(future_response, timeout=5.0)
    #         except asyncio.TimeoutError:
    #             raise HTTPException(status_code=500, detail={
    #                 'RabbitMQ': 'No response received within the timeout period.'
    #             })
    #         return response

