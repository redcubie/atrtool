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


class Teq15(ProtocolBase):
    _proto = 15
    # infobytes = [{}]
    """
    # Not really a protocol, but defines interface parameters.
    """

    def __init__(self) -> None:
        super().__init__()
        self.infobytes = [{}]

    class ClockStop(Enum):
        NOT_SUPPORTED = 0b00
        STATE_L = 0b01
        STATE_H = 0b10
        NO_PREFERENCE = 0b11

    @property
    def clock_stop(self):
        if "TA" not in self.infobytes[0] or self.infobytes[0]["TA"] is None:
            return None
        byte: bytes = self.infobytes[0]["TA"]
        bits: int = (byte[0] >> 6) & 0b11
        return self.ClockStop(bits)

    @clock_stop.setter
    def clock_stop(self, value: ClockStop):
        if not isinstance(value, self.ClockStop):
            if value is None:
                if "TA" in self.infobytes[0]:
                    self.infobytes[0].pop("TA")
                return
            raise TypeError
        if "TA" not in self.infobytes[0] or self.infobytes[0]["TA"] is None:
            oldval = 0
        else:
            oldval = int.from_bytes(self.infobytes[0]["TA"])

        newval = (oldval & 0b00111111) | ((value.value & 0b11) << 6)

        self.infobytes[0]["TA"] = newval.to_bytes()

    class CardClass(Flag):
        CLASS_A = 1
        CLASS_B = 2
        CLASS_C = 4

    @property
    def card_class(self):
        if "TA" not in self.infobytes[0] or self.infobytes[0]["TA"] is None:
            return None
        byte: bytes = self.infobytes[0]["TA"]
        assert (byte[0] >> 3) & 0b111 == 0b000
        bits: int = byte[0] & 0b111
        return self.CardClass(bits)

    @card_class.setter
    def card_class(self, value: CardClass):
        if not isinstance(value, self.CardClass):
            if value is None:
                if "TA" in self.infobytes[0]:
                    self.infobytes[0].pop("TA")
                return
            raise TypeError
        if "TA" not in self.infobytes[0] or self.infobytes[0]["TA"] is None:
            oldval = 0
        else:
            oldval = int.from_bytes(self.infobytes[0]["TA"])

        newval = (oldval & 0b11000000) | (value.value & 0b00111111)

        self.infobytes[0]["TA"] = newval.to_bytes()

    @property
    def SPU(self):
        if "TC" not in self.infobytes[0] or self.infobytes[0]["TC"] is None:
            return None
        byte: bytes = self.infobytes[0]["TC"]
        return byte

    @SPU.setter
    def SPU(self, value: bytes):
        if not isinstance(value, bytes):
            if value is None:
                if "TC" in self.infobytes[0]:
                    self.infobytes[0].pop("TC")
                return
            raise TypeError
        if len(value) != 1:
            raise ValueError
        self.infobytes[0]["TC"] = value


PROTOLIST = {0: Teq0, 1: Teq1, 15: Teq15}
