from enum import Enum
import ctypes
from . classes import ATR_Byte_Base

class ParamByteBase(ATR_Byte_Base):
    pass

class TX(ParamByteBase):
    """
    Generic parameter byte. Encodes one 8-bit unsigned integer.
    """
    _fields_ = [('_byte', ctypes.c_ubyte, 8),]

class TA1(ParamByteBase):
    """
    Encodes preferred F, fmax and D values.
    """
    _fields_ = [
        ('_Fi', ctypes.c_ubyte, 4),
        ('_Di', ctypes.c_ubyte, 4),
    ]

    Fi_options = {
        0b0000: 372,    # max f= 4MHz
        0b0001: 372,    # max f= 5MHz
        0b0010: 558,    # max f= 6MHz
        0b0011: 774,    # max f= 8MHz
        0b0100: 1116,   # max f=12MHz
        0b0101: 1488,   # max f=16MHz
        0b0110: 1860,   # max f=20MHz
        0b1001: 512,    # max f= 5MHz
        0b1010: 768,    # max f=7.5MHz
        0b1011: 1024,   # max f=10MHz
        0b1100: 1536,   # max f=15MHz
        0b1101: 2048,   # max f=20MHz
    }

    Di_options = {
        0b0001: 1,
        0b0010: 2,
        0b0011: 4,
        0b0100: 8,
        0b0101: 16,
        0b0110: 32,
        0b0111: 64,
        0b1000: 12,
        0b1001: 20,
    }

    @property
    def F(self) -> int:
        return TA1.Fi_options[self._Fi]

    # @F.setter
    # def F(self, value: int) -> None:
    #     if not isinstance(value, int):
    #         raise TypeError
        
    #     # for fi, f in TA1.Fi_options.items():
    #     #     if not 0 <= value <= 15:
    #     #         raise ValueError("K must be in range [0;15]")

    #     self._K = value

    @property
    def Fi(self) -> int:
        return self._Fi

    @Fi.setter
    def Fi(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value not in TA1.Fi_options.keys():
            raise ValueError

        self._Fi = value

    @property
    def D(self) -> int:
        return TA1.Di_options[self._Di]

    # @F.setter
    # def F(self, value: int) -> None:
    #     if not isinstance(value, int):
    #         raise TypeError
        
    #     # for fi, f in TA1.Fi_options.items():
    #     #     if not 0 <= value <= 15:
    #     #         raise ValueError("K must be in range [0;15]")

    #     self._K = value

    @property
    def Di(self) -> int:
        return self._Di

    @Di.setter
    def Di(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value not in TA1.Di_options.keys():
            raise ValueError

        self._Di = value

