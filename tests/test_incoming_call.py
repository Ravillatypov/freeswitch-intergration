from datetime import datetime

import pytest

from app.event_handlers import process_event
from app.misc.consts import CallState, CallType
from .fixtures.incoming_success import events
from app.models import Call


@pytest.mark.asyncio
async def test_incoming_success_call(db):
    assert await Call.all().count() == 0
    await process_event(events[0], None)
    assert await Call.all().count() == 1

    for event in events[1:6]:
        await process_event(event, None)

    call = await Call.first()
    assert call.state == CallState.new
    assert call.voice_started_at is None

    await process_event(events[7], None)
    call = await Call.first()
    assert call.state == CallState.connected
    assert call.request_pin == '1000'
    assert isinstance(call.voice_started_at, datetime)
    assert call.voice_finished_at is None

    for event in events[7:]:
        await process_event(event, None)

    call = await Call.first()
    assert call.state == CallState.end
    assert isinstance(call.finished_at, datetime)
    assert isinstance(call.voice_finished_at, datetime)
    assert isinstance(call.voice_started_at, datetime)
    assert call.is_hidden is False
    assert call.is_record is False
