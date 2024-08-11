from . classes import *

from enum import Flag


class ProtocolBase:
    _proto: int
    infobytes: list

    def __init__(self) -> None:
        self.infobytes = []

    @property
    def proto_num(self):
        return self._proto

