from app.misc.types import FSEvent
from .channel_callstate import channel_call_state
from .channel_create import channel_create
from .channel_destroy import channel_destroy
from .record_stop import record_stop

__all__ = ['process_event']

event_handlers = {
    'CHANNEL_CREATE': channel_create,
    'CHANNEL_CALLSTATE': channel_call_state,
    'RECORD_STOP': record_stop,
    'CHANNEL_DESTROY': channel_destroy,
}


async def process_event(event: FSEvent, rabbit_mq):
    handler = event_handlers.get(event.name)

    if handler is not None:
        await handler(event, rabbit_mq)
