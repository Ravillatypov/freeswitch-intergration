import logging
import traceback
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from types import MappingProxyType

import fast_json
from aiomisc.io import async_open
from aiomisc.log import JSONLogFormatter as BaseJsonFormatter

from app.settings import LOG_LEVEL, DATA_PATH

__all__ = ['get_logger']
_loggers = {}


class JSONLogFormatter(BaseJsonFormatter):
    def format(self, record: logging.LogRecord):
        record_dict = MappingProxyType(record.__dict__)

        data = dict(errno=0 if not record.exc_info else 255)

        for key, value in self.FIELD_MAPPING.items():
            mapping, field_type = value

            v = record_dict.get(key)

            if not isinstance(v, field_type):
                v = field_type(v)

            data[mapping] = v

        for key in record_dict:
            if key in data or key[0] == "_":
                continue

            value = record_dict[key]

            if value is None:
                continue

            data[key] = value

        for idx, item in enumerate(data.pop('args', [])):
            data['argument_%d' % idx] = str(item)

        payload = {
            'fields': data,
            'msg': record.getMessage(),
            'level': self.LEVELS[record.levelno],
        }

        if isinstance(record.msg, dict):
            data['message_raw'] = ''
            payload['msg'] = record.msg

        if self.datefmt:
            payload['timestamp'] = self.formatTime(record, self.datefmt)

        if record.exc_info:
            payload['stackTrace'] = "\n".join(
                traceback.format_exception(*record.exc_info)
            )

        return fast_json.dumps(payload, ensure_ascii=False, default=str)


def get_logger(name: str) -> Logger:
    logger = _loggers.get(name)
    if logger:
        return logger

    handler = TimedRotatingFileHandler(f'{DATA_PATH}/logs/{name}.log', when='D', backupCount=10)
    handler.setFormatter(JSONLogFormatter())
    logger = Logger(name, LOG_LEVEL)
    logger.handlers = []
    logger.addHandler(handler)

    return logger


async def capture_message(msg: str):
    async with async_open(f'{DATA_PATH}/logs/messages.txt', 'a') as f:
        await f.write(msg)
