from asyncio import sleep

from aio_pika import IncomingMessage
from aio_pika import RobustConnection
from aiomisc.service.base import Service

from app.misc.exceptions import RabbitMQNotConnected


class BaseQueueService(Service):
    queue_name: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rabbit_mq = None
        self.s3client = None

    async def start(self):
        for _ in range(100):
            self.rabbit_mq = await self.context['rabbit_mq']
            if isinstance(self.rabbit_mq, RobustConnection):
                break
            await sleep(0.1)

        self.rabbit_mq = await self.context['rabbit_mq']
        if not isinstance(self.rabbit_mq, RobustConnection):
            raise RabbitMQNotConnected

        self.s3client = await self.context['s3client']

        async with self.rabbit_mq:
            channel = await self.rabbit_mq.channel()
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
