from aiohttp import ClientSession

from app.models import Call
from app.settings import TELEPHONY_URL, ENVIRONMENT
from app.utils.logging import get_logger

logger = get_logger('root')

try:
    import ujson as json
except ImportError:
    import json


async def send_event(call: Call):
    if ENVIRONMENT == 'test' or not TELEPHONY_URL:
        return

    data = {
        'id': f'{call.id}',
        'call_type': call.call_type,
        'state': call.state,
        'sign': call.sign,
    }
    async with ClientSession(json_serialize=json.dumps) as session:
        async with session.post(TELEPHONY_URL, json=data) as resp:
            if resp.status >= 400:
                logger.warning(f'Telephony event is not send. status: {resp.status}')
