from datetime import datetime
from typing import List

from tortoise import fields
from tortoise.models import Model

from .company import Company


class VATSClient(Model):
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True, null=True)
    company: fields.ForeignKeyRelation[Company] = fields.ForeignKeyField(
        model_name='models.Company',
        related_name='vats',
    )
    client_id: str = fields.CharField(max_length=100)
    client_sign: str = fields.CharField(max_length=100)
    admin_login: str = fields.CharField(max_length=35, default='')
    admin_password: str = fields.CharField(max_length=35, default='')
    admin_domain: str = fields.CharField(max_length=35, default='', null=True)
    days_store_records: int = fields.IntField(default=None, null=True)
    operator: str = fields.CharField(default='RT', max_length=15)
    phones: List[str] = fields.JSONField(default=[])
    is_active: bool = fields.BooleanField(default=True)
    last_seen: datetime = fields.DatetimeField(null=True)
    is_blacklist: bool = fields.BooleanField(default=True)
    blacklist: List[str] = fields.JSONField(default=[])
    robot_username: str = fields.CharField(max_length=50, default='')
    robot_password: str = fields.CharField(max_length=50, default='')
    comment: str = fields.TextField(default='')

    class Meta:
        table = 'vats'
