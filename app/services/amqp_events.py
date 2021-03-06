from aio_pika import IncomingMessage

from app.event_handlers import process_event
from app.settings import MQ_EVENTS_QUEUE_NAME, EVENT_CAPTURE
from app.misc.types import FSEvent
from .base import BaseQueueService
from app.utils.logging import get_logger, capture_message

logger = get_logger('root')
mq_log = get_logger('amqp')


class AMQPService(BaseQueueService):
    queue_name = MQ_EVENTS_QUEUE_NAME

    async def process(self, message: IncomingMessage):
        async with message.process():
            try:
                if EVENT_CAPTURE:
                    await capture_message(message.body.decode())

                event = FSEvent(message.body)
                await process_event(event, self.rabbit_mq)
            except Exception as e:
                logger.warning(f'Exception on process event: {e}')
                mq_log.warning(message.body.decode())
