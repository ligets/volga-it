import asyncio

import aio_pika
from fastapi import HTTPException


class RabbitMQBaseClient:
    def __init__(self, rabbitmq_url='amqp://guest:guest@localhost/'):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None

    async def connect(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        return self.connection

    async def close(self):
        if self.connection is not None and not self.connection.is_closed:
            await self.connection.close()

    async def _publish_message(self, channel, body: bytes, routing_key: str, correlation_id: str, reply_to: str):
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=body,
                correlation_id=correlation_id,
                reply_to=reply_to,
            ),
            routing_key=routing_key
        )

    async def _wait_for_response(self, callback_queue, correlation_id: str, timeout: float = 5.0):
        loop = asyncio.get_running_loop()
        future_response = loop.create_future()

        async def on_response(msg: aio_pika.abc.AbstractIncomingMessage):
            async with msg.process():
                if msg.correlation_id == correlation_id:
                    future_response.set_result(msg.body)

        await callback_queue.consume(on_response)

        try:
            response = await asyncio.wait_for(future_response, timeout=timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=500, detail={
                'RabbitMQ': 'No response received within the timeout period.'
            })

        return response

    async def create_channel_and_queue(self):
        channel = await self.connection.channel()
        callback_queue = await channel.declare_queue(auto_delete=True)
        return channel, callback_queue
