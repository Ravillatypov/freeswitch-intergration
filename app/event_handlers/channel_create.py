from datetime import datetime

from app.misc.consts import CallType, CallState
from app.misc.types import FSEvent
from app.models import Call, VATSClient
from app.utils.events import is_external, is_internal, phone_number_normalize
from app.utils.logging import get_logger

logger = get_logger('root')


async def channel_create(event: FSEvent, *args, **kwargs):
    call = await Call.get_or_none(operator_session_id=event.call_uuid, operator='MDO')

    if call:
        return

    vats: VATSClient = await VATSClient.get_or_none(id=event.vats_id)
    if not vats:
        logger.warning(f'VATS is not found. domain: {event.vats_id}')
        return

    from_ = event.get('Caller-Caller-ID-Number')
    to = event.get('Caller-Destination-Number')
    from_num, from_pin, request_num, request_pin = '', '', '', ''

    if is_external(from_) and is_external(to):
        from_num, request_num = phone_number_normalize(from_), phone_number_normalize(to)
        call_type = CallType.incoming
    elif is_internal(from_) and is_external(to):
        from_pin, request_num = from_, phone_number_normalize(to)
        from_num = phone_number_normalize(event.gateway)
        call_type = CallType.outbound
    elif is_internal(from_) and is_internal(to):
        from_pin, request_pin = from_, to
        from_num, request_num = phone_number_normalize(event.gateway), phone_number_normalize(event.gateway)
        call_type = CallType.internal
    else:
        from_num, from_pin = phone_number_normalize(from_), from_
        request_num, request_pin = phone_number_normalize(to), to
        call_type = CallType.not_defined

    call = await Call.create(
        operator_session_id=event.call_uuid,
        operator='MDO',
        from_number=from_num,
        request_number=request_num,
        state=CallState.new,
        started_at=datetime.fromtimestamp(event.timestamp),
        company_id=vats.company_id,
        from_pin=from_pin,
        request_pin=request_pin,
        call_type=call_type,
    )

    call.is_hidden = vats.call_is_hidden(call)

    await call.save()
