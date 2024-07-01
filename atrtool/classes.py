from enum import Enum
import ctypes
import struct


class ATR_Byte_Base(ctypes.BigEndianStructure):
    def __repr__(self) -> str:
        return '{:08b}'.format(struct.unpack_from('!B', self)[0])

class TS(ATR_Byte_Base):
    """
    Initial character. Encodes bit-order of all following bytes.
    """
    _fields_ = [
        ('_a', ctypes.c_ubyte, 3),
        ('_bitorder', ctypes.c_ubyte, 3),
        ('_b', ctypes.c_ubyte, 2),
    ]

    class BitOrder(Enum):
        LSB_first = 0
        MSB_first = 1
    _bitorder_e: BitOrder

    def __init__(self, bitorder: BitOrder = None) -> None:
        super().__init__()
        self._a = 0b110
        self._b = 0b00
        if bitorder and isinstance(bitorder, self.BitOrder):
            self.bitorder = bitorder
        else:
            self.bitorder = self.BitOrder.MSB_first

    @property
    def bitorder(self):
        return self._bitorder_e

    @bitorder.setter
    def bitorder(self, value: BitOrder):
        if not isinstance(value, self.BitOrder):
            raise TypeError
        self._bitorder_e = value
        if value == self.BitOrder.LSB_first:
            self._bitorder = 0b000
        else:
            self._bitorder = 0b111
