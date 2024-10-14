import asyncio
import json
import uuid
from functools import partial

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

    async def _publish_message(self, channel, body: bytes, routing_key: str):
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=body
            ),
            routing_key=routing_key
        )

