from app.misc.types import FSEvent
from app.models import Call
from app.misc.consts import CallState, CallType
from datetime import datetime
from math import ceil


async def channel_destroy(event: FSEvent, *args, **kwargs):
    if event.call_uuid != event.get('Unique-ID'):
        return

    call = await Call.get_or_none(operator_session_id=event.call_uuid, operator='MDO')

    if not call:
        return

    call.finished_at = datetime.fromtimestamp(event.timestamp)
    call.voice_finished_at = call.finished_at if call.voice_started_at else None

    if call.voice_finished_at:
        call.state = CallState.end
        delta = call.voice_finished_at - call.voice_started_at
        call.duration_sec = delta.total_seconds()
        call.duration_min = ceil(call.duration_sec / 60)
    elif call.call_type == CallType.incoming:
        call.state = CallState.missed
    else:
        call.state = CallState.not_connected

    await call.save()
