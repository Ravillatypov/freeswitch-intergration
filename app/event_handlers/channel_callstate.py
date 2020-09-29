from datetime import datetime

from app.misc.consts import CallState, CallType
from app.misc.types import FSEvent
from app.models import Call, VATSClient


async def channel_call_state(event: FSEvent, *args, **kwargs):
    if not (event.bridged_timestamp or event.call_uuid != event.uuid):
        return

    call = await Call.get_or_none(operator_session_id__in=event.call_uuid_list, operator='MDO')

    if not call:
        return

    if call.call_type == CallType.incoming and event.get('Caller-Callee-ID-Number'):
        call.request_pin = event.get('Caller-Callee-ID-Number')

    if event.bridged_timestamp:
        call.state = CallState.connected
        call.voice_started_at = datetime.fromtimestamp(event.bridged_timestamp)

    vats = await VATSClient.get_or_none(company_id=call.company_id, operator='MDO')
    if vats:
        call.is_hidden = vats.call_is_hidden(call)

    await call.save()
