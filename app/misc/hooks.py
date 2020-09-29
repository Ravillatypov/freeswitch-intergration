from typing import Type

from aio_pika import connect_robust
from aiomisc.entrypoint import Entrypoint
from tortoise import Tortoise
from tortoise.signals import post_save

from app.misc.s3client import S3Client
from app.models import Call
from app.settings import (DB_DSN, MQ_DSN, S3_BUCKET_NAME, S3_FOLDER_NAME, AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION,
                          AWS_SECRET_ACCESS_KEY)
from app.utils.telephony import send_event


async def on_start(entrypoint: Entrypoint, *args, **kwargs):
    await Tortoise.init(
        db_url=DB_DSN,
        modules={'models': ['app.models']},
    )
    entrypoint.ctx['rabbit_mq'] = await connect_robust(MQ_DSN)
    entrypoint.ctx['s3client'] = S3Client(S3_BUCKET_NAME, S3_FOLDER_NAME, AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION)


async def on_stop(entrypoint: Entrypoint, *args, **kwargs):
    await Tortoise.close_connections()
    await entrypoint.ctx['rabbit_mq'].close()


@post_save(Call)
async def telephony_hook(sender: Type[Call], instance: Call, created: bool, *args):
    if not created:
        await send_event(instance)
