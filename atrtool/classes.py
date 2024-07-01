from enum import Enum
import ctypes
import struct


class ATR_Byte_Base(ctypes.BigEndianStructure):
    def __repr__(self) -> str:
        return '{:08b}'.format(struct.unpack_from('!B', self)[0])

