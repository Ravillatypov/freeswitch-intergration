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
    def timestamp(self) -> int:
        return int(self.__event.get('Event-Date-Timestamp'))

    @property
    def bridged_timestamp(self) -> int:
        return int(self.__event.get('Caller-Channel-Bridged-Time'))

    def get(self, key: str, default: Any = '') -> str:
        return self.__event.get(key, default)
