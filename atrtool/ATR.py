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

    def to_bytes(self) -> bytes:
        data = bytearray()

        data += self.TS.to_bytes()

        t0 = T0()
        ta1 = self.params["TA1"].to_bytes() if "TA1" in self.params else b''
        tb1 = self.params["TB1"].to_bytes() if "TB1" in self.params else b''
        tc1 = self.params["TC1"].to_bytes() if "TC1" in self.params else b''
        hist_bytes = self.hist_bytes
        t0.K = len(hist_bytes)
        # T0 is added later, when we can figure out if any data will follow it

        data2 = bytearray()

        ta = self.params["TA2"].to_bytes() if "TA2" in self.params else b''
        tb = self.params["TB2"].to_bytes() if "TB2" in self.params else b''
        tc = self.protocols[0].waiting_time.to_bytes() \
            if 0 in self.protocols and self.protocols[0].waiting_time is not None \
            else b''
        td = TD()
        need_commit = False
        protocols = self.protocols.copy()
        if protocols:
            first_proto = True
            proto = sorted(protocols.keys())[0]  # get first enabled protocol
            if proto == 0:  # T=0 doesn't have any more interface bytes, so if it has been hit, it must be ignored in the loop
                protocols.pop(0)
                first_proto = False # T=0 is first, not loop first iteration, so it must be set here
            td.T = proto
            need_commit = True
            for proto, info in protocols.items():
                infobytes = info.infobytes
                if first_proto:
                    first_proto = False
                    if not any(infobytes): # if protocol is the first one and has no parameters, then subsequent parameter bytes can be skipped
                        continue

                num_without_data = 0
                for x in infobytes:
                    if need_commit:
                        td.set_Y(ta, tb, tc, 1)
                        data2 += td.to_bytes()
                        data2 += ta+tb+tc
                        need_commit = False

                    td = TD()
                    td.T = proto
                    ta = x["TA"] if "TA" in x else b''
                    tb = x["TB"] if "TB" in x else b''
                    tc = x["TC"] if "TC" in x else b''

                    if not any([ta, tb, tc]):
                        num_without_data += 1
                        continue

                    for i in range(num_without_data):
                        # generate TD with no ta,tb,tc
                        td_2 = TD()
                        td_2.T = proto
                        td_2.set_Y(0, 0, 0, 1)
                        data2 += td_2
                    num_without_data = 0
                    need_commit = True

                if num_without_data == len(infobytes):
                    ta = b''
                    tb = b''
                    tc = b''
                    td.set_Y(ta, tb, tc, 1)
                    need_commit = True

        if need_commit:
            td.set_Y(ta, tb, tc, 0)
            data2 += td.to_bytes()
            data2 += ta+tb+tc

        if data2:
            t0.set_Y(ta1, tb1, tc1, True)
        else:
            t0.set_Y(ta1, tb1, tc1, False)

        data += t0.to_bytes()
        data += ta1+tb1+tc1

        data += data2

        data += hist_bytes

        checksum = calc_TCK(data[1:])
        data.append(checksum)

        return bytes(data)


def calc_TCK(ins: Iterable[int]) -> int:
    val = 0
    for x in ins:
        val ^= x

    return 0x00 ^ val
