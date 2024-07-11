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


class T0(ATR_Byte_Base):
    """
    Format byte. Encodes indicator Y1 and historical byte count K.
    """
    _fields_ = [
        ('_Y', ctypes.c_ubyte, 4),
        ('_K', ctypes.c_ubyte, 4),
    ]

    def __init__(self, Y: int = None, K: int = None) -> None:
        super().__init__()
        if Y is not None:
            self.Y = Y
        if K is not None:
            self.K = K

    @property
    def Y(self):
        return self._Y

    @Y.setter
    def Y(self, value: int):
        raise NotImplementedError
    
    def set_Y(self, TA: bool = False, TB: bool = False, TC: bool = False, TD: bool = False):
        flags = [TA, TB, TC, TD]
        # if any(not isinstance(x, bool) for x in (TA, TB, TC, TD)):
        #     raise TypeError
        for i, x in enumerate(flags):
            if not isinstance(x, bool):
                try:
                    flags[i] = bool(x)
                except:
                    raise TypeError
                
        newval = 0
        for i, x in enumerate(flags):
            if x:
                newval |= 1<<i

        self._Y = newval

    @property
    def K(self):
        return self._K
    
    @K.setter
    def K(self, value: int):
        if not isinstance(value, int):
            raise TypeError
        if not 0 <= value <= 15:
            raise ValueError("K must be in range [0;15]")
        
        self._K = value

