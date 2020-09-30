from datetime import datetime

import pytest

from app.event_handlers import process_event
from app.misc.consts import CallState, CallType
from .fixtures.internal_connected import events as success_events
from .fixtures.internal_not_connected import events as not_connected_events
from app.models import Call


@pytest.mark.asyncio
async def test_internal_success_call(db):
    assert await Call.all().count() == 0
    await process_event(success_events[0], None)
    assert await Call.all().count() == 1

    call = await Call.first()
    assert call.state == CallState.new
    assert call.call_type == CallType.internal
    assert call.voice_started_at is None
    assert call.from_pin == '1001'
    assert call.from_number == '78432054455'
    assert call.request_number == '78432054455'
    assert call.request_pin == '1000'

    for event in success_events[1:8]:
        await process_event(event, None)

    call = await Call.first()
    assert call.state == CallState.connected
    assert isinstance(call.voice_started_at, datetime)
    assert call.voice_finished_at is None

    for event in success_events[8:]:
        await process_event(event, None)

    call = await Call.first()
    assert call.state == CallState.end
    assert isinstance(call.finished_at, datetime)
    assert isinstance(call.voice_finished_at, datetime)
    assert isinstance(call.voice_started_at, datetime)
    assert call.is_hidden is False
    assert call.is_record is False


@pytest.mark.asyncio
async def test_internal_not_connected_call(db):
    assert await Call.all().count() == 0
    await process_event(not_connected_events[0], None)
    assert await Call.all().count() == 1

    for event in not_connected_events[1:3]:
        await process_event(event, None)

    call = await Call.first()
    assert call.state == CallState.new
    assert call.call_type == CallType.internal
    assert call.from_pin == '1000'
    assert call.from_number == '78432054455'
    assert call.request_number == '78432054455'
    assert call.request_pin == '1001'
    assert call.voice_started_at is None

    for event in not_connected_events[3:]:
        await process_event(event, None)

    call = await Call.first()
    assert call.from_pin == '1000'
    assert call.request_pin == '1001'
    assert call.state == CallState.not_connected
    assert isinstance(call.finished_at, datetime)
    assert call.voice_finished_at is None
    assert call.voice_started_at is None
    assert call.is_hidden is False
    assert call.is_record is False
