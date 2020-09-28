from datetime import datetime
from typing import List

from tortoise import fields
from tortoise.models import Model


class Company(Model):
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True, null=True)
    name: str = fields.CharField(max_length=50, default='')

    class Meta:
        table = 'company'


class Staff(Model):
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True, null=True)
    company: fields.ForeignKeyRelation[Company] = fields.ForeignKeyField(
        model_name='models.Company',
        related_name='staff',
    )
    user_id: int = fields.IntField(unique=True)
    phone_pin: str = fields.CharField(max_length=50, default='')
    room_id: List[int] = fields.JSONField(default=[])
    key: str = fields.CharField(max_length=50, default='', unique=True)  # api token

    class Meta:
        table = "company_staff"
