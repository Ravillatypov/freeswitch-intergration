from sys import exit

from app.misc.consts import CallState, CallType
from app.misc.hooks import on_stop, on_start
from app.models import *

__all__ = ['Company', 'Call', 'CallRecord', 'VATSClient', 'Staff', 'CallState', 'CallType', 'on_start']


async def _exit():
    await on_stop()
    exit(0)
