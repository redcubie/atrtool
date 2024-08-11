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

