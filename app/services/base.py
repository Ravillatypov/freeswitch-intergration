from aio_pika import IncomingMessage
from aio_pika import RobustConnection
from aiomisc.service.base import Service

from app.misc.exceptions import RabbitMQNotConnected


class BaseQueueService(Service):
    queue_name: str = None

    async def start(self):
        if not isinstance(self.context['rabbit_mq'], RobustConnection):
            raise RabbitMQNotConnected

        async with self.context['rabbit_mq']:
            channel = await self.context['rabbit_mq'].channel()
            queue = await channel.declare_queue(
                name=self.queue_name,
                durable=True,
            )

            async with queue.iterator() as iterator:
                async for message in iterator:
                    await self.process(message)

    @staticmethod
    async def process(message: IncomingMessage):
        raise NotImplementedError
