import pytest

from app.event_handlers import process_event
from app.misc.consts import CallState, CallType
from .fixtures.incoming_success import events
from app.models import Call


@pytest.mark.asyncio
async def test_channel_create_called(db):
    assert await Call.all().count() == 0
    await process_event(events[0], None)
    assert await Call.all().count() == 1

    call = await Call.first()
    assert call.from_number == '79179078642'
    assert call.from_pin == ''
    assert call.request_pin == ''
    assert call.request_number == '78432054455'
    assert call.state == CallState.new
    assert call.call_type == CallType.incoming

    await process_event(events[2], None)
    assert await Call.all().count() == 1
