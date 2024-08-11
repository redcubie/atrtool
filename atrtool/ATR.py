from typing import Iterable
from . classes import *
from . protocols import *
from . params import *


class ATR:
    TS: TS
    protocols: dict[str, ProtocolBase]
    hist_bytes: bytes  # TODO: convert to parameter?
    params: dict[str, ParamByteBase]

    def __init__(self) -> None:
        self.protocols = {}
        self.params = {}
        self.hist_bytes = b""

    @classmethod
    def from_bytes(cls: "type[ATR]", data: bytes) -> "ATR":
        inst = cls()

        offset = 0

        byte = data[offset:offset+1]
        inst.TS = TS.from_bytes(byte)
        assert inst.TS.check_validity()
        offset += 1

        byte = data[offset:offset+1]
        t0 = T0.from_bytes(byte)
        num_hist_bytes = t0.K
        bytes_available = t0.get_Y()
        offset += 1

        if bytes_available["TA"]:
            byte = data[offset:offset+1]
            inst.params["TA1"] = TA1.from_bytes(byte)
            offset += 1
        if bytes_available["TB"]:
            byte = data[offset:offset+1]
            inst.params["TB1"] = TX.from_bytes(byte)
            offset += 1
        if bytes_available["TC"]:
            byte = data[offset:offset+1]
            inst.params["TC1"] = TC1.from_bytes(byte)
            offset += 1

        # read TA/TB/TC _2 as global
        TD_available = bytes_available["TD"]
        if TD_available:
            byte = data[offset:offset+1]
            this_TD = TD.from_bytes(byte)
            bytes_available = this_TD.get_Y()
            offset += 1

            if bytes_available["TA"]:
                byte = data[offset:offset+1]
                inst.params["TA2"] = TA2.from_bytes(byte)
                offset += 1
            if bytes_available["TB"]:
                byte = data[offset:offset+1]
                inst.params["TB2"] = TX.from_bytes(byte)
                offset += 1
            if bytes_available["TC"]:
                byte = data[offset:offset+1]
                if 0 not in inst.protocols:
                    proto_inst = Teq0()
                    proto_inst.waiting_time = int.from_bytes(byte, 'big')
                    inst.protocols[0] = proto_inst
                offset += 1

            proto = this_TD.T
            if proto not in inst.protocols:
                proto_inst = PROTOLIST[proto]()
                inst.protocols[proto] = proto_inst

        proto_iters = {}
        TD_available = bytes_available["TD"]
        while TD_available:
            byte = data[offset:offset+1]
            this_TD = TD.from_bytes(byte)
            bytes_available = this_TD.get_Y()
            offset += 1

            proto = this_TD.T

            if proto not in inst.protocols:
                proto_inst = PROTOLIST[proto]()
                inst.protocols[proto] = proto_inst
                proto_iters[proto] = 0

            iternum = proto_iters[proto]

            for x in ("TA", "TB", "TC"):
                if not bytes_available[x]:
                    continue
                byte = data[offset:offset+1]
                inst.protocols[proto].infobytes[iternum][x] = byte
                offset += 1

            proto_iters[proto] += 1

            TD_available = bytes_available["TD"]

        inst.hist_bytes = data[offset:offset+num_hist_bytes]
        offset += num_hist_bytes

        # check checksum
        checksum = calc_TCK(data[1:offset])
        assert checksum == data[offset]
        offset += 1

        # make sure counts of consumed bytes and input bytes are equal
        assert offset == len(data)

        return inst

def calc_TCK(ins: Iterable[int]) -> int:
    val = 0
    for x in ins:
        val ^= x

    return 0x00 ^ val
