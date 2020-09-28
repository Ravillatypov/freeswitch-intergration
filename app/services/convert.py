from pathlib import Path

import ffmpeg
from aio_pika import IncomingMessage
from aiomisc import threaded

from app.models import Call
from app.settings import MQ_CONVERTER_QUEUE_NAME, DATA_PATH, RECORDS_PATH_PREFIX
from app.utils.logging import get_logger
from app.utils.rabbit import need_upload
from .base import BaseQueueService

logger = get_logger('root')


@threaded
def convert_record(source: str, destination: str) -> bool:
    try:
        stream = ffmpeg.input(source)
        stream = ffmpeg.output(stream, destination)
        ffmpeg.run(stream)
    except Exception as err:
        logger.warning(f'{err}')
    return Path(destination).exists()


class ConvertService(BaseQueueService):
    queue_name = MQ_CONVERTER_QUEUE_NAME

    async def process(self, message: IncomingMessage):
        async with message.process():
            call_id, path = message.body.decode().splitlines()

            call = await Call.get_or_none(id=call_id)
            if not call:
                logger.warning(f'Bad call_id: {call_id}. Call not found')
                return

            source = path.replace(RECORDS_PATH_PREFIX, f'{DATA_PATH}/fs_records')
            destination = f'{DATA_PATH}/converted_records/{call_id}.mp3'

            if not Path(source).exists():
                logger.warning(f'Record file not found. File: {source}')
                return

            if not await convert_record(
                    source=source,
                    destination=destination,
            ):
                logger.warning(f'Record not converted. File: {source}')
                return

            await need_upload(self.rabbit_mq, call_id, destination)
