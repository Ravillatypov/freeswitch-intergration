from datetime import datetime

from app.misc.consts import CallType, CallState
from app.misc.types import FSEvent
from app.models import Call, VATSClient
from app.settings import logger
from app.utils.events import is_external, is_internal


async def channel_create(event: FSEvent, *args, **kwargs):
    call = await Call.get_or_none(operator_session_id=event.call_uuid, operator='FS')

    if call:
        return

    domain = event.get('variable_domain_name')
    default_gateway = event.get('variable_sip_gateway_name') or event.get('variable_default_gateway')
    vats = await VATSClient.get_or_none(admin_domain=domain)
    if not vats:
        logger.warning(f'VATS is not found. domain: {domain}')

    from_ = event.get('Caller-Caller-ID-Number')
    to = event.get('Caller-Destination-Number')
    from_num, from_pin, request_num, request_pin = '', '', '', ''

    if is_external(from_) and is_external(to):
        from_num, request_num = from_, to
        call_type = CallType.incoming
    elif is_internal(from_) and is_external(to):
        from_pin, request_num = from_, to
        from_num = default_gateway
        call_type = CallType.outbound
    elif is_internal(from_) and is_internal(to):
        from_pin, request_pin = from_, to
        from_num, request_num = default_gateway, default_gateway
        call_type = CallType.internal
    else:
        from_num, from_pin, request_num, request_pin = from_, from_, to, to
        call_type = CallType.not_defined

    await Call.create(
        operator_session_id=event.call_uuid,
        operator='FS',
        from_number=from_num,
        request_number=request_num,
        state=CallState.new,
        started_at=datetime.fromtimestamp(event.timestamp),
        company=vats.company,
        from_pin=from_pin,
        request_pin=request_pin,
        call_type=call_type,
    )
