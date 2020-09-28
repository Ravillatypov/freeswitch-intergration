from aio_pika import IncomingMessage

from app.event_handlers import process_event
from app.settings import MQ_EVENTS_QUEUE_NAME
from app.misc.types import FSEvent
from .base import BaseQueueService


class AMQPService(BaseQueueService):
    queue_name = MQ_EVENTS_QUEUE_NAME

    @staticmethod
    async def process(message: IncomingMessage):
        async with message.process():
            event = FSEvent(message.body)
            await process_event(event)
