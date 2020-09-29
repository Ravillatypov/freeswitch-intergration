from typing import Any, Union

try:
    import ujson as json
except ImportError:
    import json


class FSEvent:

    def __init__(self, data: Union[bytes, dict], *args, **kwargs):
        if isinstance(data, bytes) or isinstance(data, str):
            self.__event = json.loads(data)
        elif isinstance(data, dict):
            self.__event = data
        else:
            self.__event = {}

    @property
    def name(self) -> str:
        return self.__event.get('Event-Name')

    @property
    def call_uuid(self) -> str:
        for key in ("Channel-Call-UUID", "Other-Leg-Unique-ID", "Caller-Unique-ID", "Unique-ID",
                    "variable_call_uuid", "variable_originating_leg_uuid", "variable_uuid",
                    "variable_originator", "variable_signal_bond"):
            if key in self.__event:
                return key

    @property
    def vats_id(self) -> int:
        context: str = self.__event.get('Caller-Context')
        _, _, _, v_id, *_ = context.split('_')
        return int(v_id)

    @property
    def company_id(self) -> int:
        context: str = self.__event.get('Caller-Context')
        _, c_id, *_ = context.split('_')
        return int(c_id)

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
