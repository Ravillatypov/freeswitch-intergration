from datetime import datetime
from typing import List, Iterable

from tortoise import fields
from tortoise.models import Model

from .call import Call
from .company import Company


def match_numbers(external_numbers: Iterable, *args) -> bool:
    for ext_num in external_numbers:
        ext_num_len = len(ext_num)
        for arg in args:
            if not isinstance(arg, str):
                continue
            arg = arg.replace('+', '').split(':')[-1].split('@')[0][-10:]
            arg_len = len(arg)
            if any((arg_len > 5 and arg == ext_num[-arg_len:],
                    arg == ext_num,
                    ext_num_len > 5 and arg[-ext_num_len:] == ext_num)):
                return True
    return False


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

    def call_is_hidden(self, call_data: Call) -> bool:
        if not self.blacklist:
            return False

        user1 = call_data.from_user
        user2 = call_data.request_user
        pin1 = call_data.from_pin
        pin2 = call_data.request_pin
        num1 = call_data.from_number
        num2 = call_data.request_number

        matched = any(
            (
                user1 and user1 in self.username_list,
                user2 and user2 in self.username_list,
                pin1 and pin1 in self.internal_numbers,
                pin2 and pin2 in self.internal_numbers,
            )
        )
        if not matched:
            matched = match_numbers(self.external_numbers, num1, num2)
        if not matched:
            matched = match_numbers(self.blacklist, user1, user2, num1, num2)
        if self.is_blacklist:
            return matched
        return not matched

    @property
    def external_numbers(self):
        return [i for i in self.blacklist if len(i) > 5]

    @property
    def username_list(self):
        res = []
        for i in self.blacklist:
            try:
                int(i)
            except Exception:
                res.append(i)
        return res
