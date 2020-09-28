from pathlib import Path

from aio_pika import IncomingMessage
from aiomisc import threaded
from aiomisc.io import async_open

from app.misc.s3client import S3Client
from app.models import Call, CallRecord
from app.settings import MQ_UPLOADS_QUEUE_NAME
from app.utils.logging import get_logger
from .base import BaseQueueService

logger = get_logger('root')


@threaded
def upload_record(s3client: S3Client, content: bytes, filename: str) -> str:
    try:
        link = s3client.upload(filename, content)
    except Exception as err:
        logger.warning(f'{err}')
        link = ''
    return link


class UploadService(BaseQueueService):
    queue_name = MQ_UPLOADS_QUEUE_NAME

    async def process(self, message: IncomingMessage):
        async with message.process():
            call_id, path = message.body.decode().splitlines()

            call = await Call.get_or_none(id=call_id)
            if not call:
                logger.warning(f'Bad call_id: {call_id}. Call not found')
                return

            if not Path(path).exists():
                logger.warning(f'Converted record file not found. File: {path}')
                return

            async with async_open(path, 'rb') as f:
                data = await f.read()

            link = await upload_record(
                self.s3client,
                data,
                call.create_record_filename(),
            )

            await CallRecord.create(
                call_id=call_id,
                file_name=link,
                attempts_count=1,
            )
