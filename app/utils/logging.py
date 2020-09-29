from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from aiomisc.log import JSONLogFormatter
from aiomisc.io import async_open

from app.settings import LOG_LEVEL, DATA_PATH

__all__ = ['get_logger']
_loggers = {}


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
