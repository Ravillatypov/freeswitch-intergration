from datetime import datetime
from hashlib import md5
from uuid import uuid4

from tortoise import fields
from tortoise.models import Model

from .company import Company


class Call(Model):
    id: uuid4 = fields.UUIDField(pk=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True, null=True)
    company: fields.ForeignKeyRelation[Company] = fields.ForeignKeyField(
        model_name='models.Company',
        related_name='calls',
        on_delete=fields.CASCADE,
    )
    operator: str = fields.CharField(max_length=15)
    operator_session_id: str = fields.CharField(max_length=50, default='', index=True)
    call_type: str = fields.CharField(max_length=15)
    state: str = fields.CharField(max_length=15)
    from_number: str = fields.CharField(max_length=256)
    from_user: str = fields.CharField(max_length=50, default='')
    from_pin: str = fields.CharField(max_length=15, default='')
    request_number: str = fields.CharField(max_length=256)
    request_user: str = fields.CharField(max_length=50, default='')
    request_pin: str = fields.CharField(max_length=50, default='')
    record_url: str = fields.CharField(max_length=250, default='')
    appeal_id: uuid4 = fields.UUIDField(null=True, default=None, index=True)
    has_appeal: bool = fields.BooleanField(null=True, default=None)
    appeal_number: int = fields.IntField(null=True, default=None)
    managed_by: int = fields.IntField(null=True)
    is_record: bool = fields.BooleanField(default=False)
    disconnect_reason: str = fields.CharField(max_length=150, default='')
    comment: str = fields.CharField(max_length=255, default='')
    managed_at: datetime = fields.DatetimeField(null=True)
    started_at: datetime = fields.DatetimeField(null=True)
    voice_started_at: datetime = fields.DatetimeField(null=True)
    voice_finished_at: datetime = fields.DatetimeField(null=True)
    finished_at: datetime = fields.DatetimeField(null=True)
    is_hidden: bool = fields.BooleanField(null=True, default=False)
    voximplant_session_id: str = fields.CharField(max_length=20, default=None, null=True)
    dialog: str = fields.TextField(default='')
    campaign_id: int = fields.IntField(null=True, default=None)
    campaign_contact_id: int = fields.IntField(null=True, default=None)
    duration_sec: int = fields.IntField(default=0)
    duration_min: int = fields.IntField(default=0)

    class Meta:
        table = 'calls'

    def create_record_filename(self):
        return str(self.id).replace('-', '') + '.mp3'

    @property
    def sign(self) -> str:
        call_str = f'{self.id}{self.call_type}{self.state}'.encode()
        return md5(call_str).hexdigest()


class CallRecord(Model):
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True, null=True)
    call: fields.ForeignKeyRelation[Call] = fields.ForeignKeyField(
        model_name='models.Call',
        related_name='records',
        on_delete=fields.CASCADE,
        unique=True
    )
    file_name: str = fields.CharField(max_length=150)
    remove_at: datetime = fields.DatetimeField(null=True)
    # download attempts count
    attempts_count: int = fields.SmallIntField(null=False, default=0)

    class Meta:
        table = 'call_records'
