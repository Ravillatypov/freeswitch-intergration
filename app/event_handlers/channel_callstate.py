from datetime import datetime

from app.misc.consts import CallState, CallType
from app.misc.types import FSEvent
from app.models import Call, VATSClient


async def channel_call_state(event: FSEvent, *args, **kwargs):
    if not event.bridged_timestamp or event.call_uuid == event.get('Unique-ID'):
        return

    call = await Call.get_or_none(operator_session_id=event.call_uuid, operator='MDO')

    if not call or call.state != CallState.new:
        return

    if call.call_type == CallType.incoming:
        call.request_pin = event.get('Caller-Callee-ID-Number')

    call.state = CallState.connected
    call.voice_started_at = datetime.fromtimestamp(event.bridged_timestamp)

    vats = await VATSClient.get_or_none(company=call.company, operator='MDO')
    if vats:
        call.is_hidden = vats.call_is_hidden(call)

    await call.save()
