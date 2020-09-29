from app.misc.types import FSEvent
from app.models import Call
from app.utils.rabbit import need_convert


async def record_stop(event: FSEvent, rabbit_mq, *args, **kwargs):
    call = await Call.get_or_none(operator_session_id__in=event.call_uuid_list, operator='MDO')

    if not call:
        return

    call.is_record = True
    call.record_url = event.get('Record-File-Path')[-250:]
    await call.save()

    await need_convert(rabbit_mq, call.id, event.get('Record-File-Path'))
