from uuid import uuid4

from aio_pika import Message

from app.settings import MQ_CONVERTER_QUEUE_NAME, MQ_UPLOADS_QUEUE_NAME
from aio_pika import RobustConnection


async def send_message(rabbit_mq: RobustConnection, routing_key: str, body: bytes):
    async with rabbit_mq:
        channel = await rabbit_mq.channel()
        await channel.default_exchange.publish(
            Message(body=body),
            routing_key=routing_key,
        )


async def need_convert(rabbit_mq: RobustConnection, call_id: uuid4, path: str):
    await send_message(
        rabbit_mq,
        body=f'{call_id}\n{path}'.encode(),
        routing_key=MQ_CONVERTER_QUEUE_NAME,
    )


async def need_upload(rabbit_mq: RobustConnection, call_id: uuid4, path: str):
    await send_message(
        rabbit_mq,
        body=f'{call_id}\n{path}'.encode(),
        routing_key=MQ_UPLOADS_QUEUE_NAME,
    )
