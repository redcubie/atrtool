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


# TODO: refactor this
class Teq0(ProtocolBase):
    _proto = 0
    pass
    waiting_time: int = None  # TODO: probably convert to parameter


class Teq1(ProtocolBase):
    _proto = 1
    # infobytes = [{}, {}]

    def __init__(self) -> None:
        super().__init__()
        self.infobytes = [{}, {}]


