from typing import Any, Union, List
from app.utils.events import is_uuid

try:
    import ujson as json
except ImportError:
    import json


class FSEvent:
    keys = ("Channel-Call-UUID", "Other-Leg-Unique-ID", "Caller-Unique-ID", "Unique-ID", "variable_call_uuid",
            "variable_originating_leg_uuid", "variable_uuid", "variable_originator", "variable_signal_bond")

    def __init__(self, data: Union[bytes, dict], *args, **kwargs):
        if isinstance(data, bytes) or isinstance(data, str):
            self.__event = json.loads(data)
        elif isinstance(data, dict):
            self.__event = data
        else:
            self.__event = {}

    def __str__(self):
        return f'{self.__event}'

    @property
    def name(self) -> str:
        return self.__event.get('Event-Name')

    @property
    def uuid(self) -> str:
        return self.__event.get('Unique-ID')

    @property
    def call_uuid(self) -> str:
        for key in self.keys:
            if is_uuid(self.__event.get(key)):
                return self.__event.get(key)
        return ''

    @property
    def call_uuid_list(self) -> List[str]:
        return [self.__event.get(k) for k in self.keys if self.__event.get(k)]

    @property
    def vats_id(self) -> int:
        try:
            vats_id: str = self.__event.get('x-vats-id')
            return int(vats_id)
        except Exception:
            pass
        return 0

    @property
    def company_id(self) -> int:
        try:
            context: str = self.__event.get('Caller-Context')
            _, c_id, *_ = context.split('_')
            return int(c_id)
        except Exception:
            pass
        return 0

    @property
    def gateway(self) -> str:
        for key in ('variable_sip_gateway_name', 'variable_default_gateway'):
            gw = self.__event.get(key)
            if gw:
                return gw
        return ''

    @property
    def timestamp(self) -> float:
        return int(self.__event.get('Event-Date-Timestamp')) / 1_000_000

    @property
    def bridged_timestamp(self) -> float:
        return int(self.__event.get('Caller-Channel-Bridged-Time')) / 1_000_000

    def get(self, key: str, default: Any = '') -> str:
        return self.__event.get(key, default)
