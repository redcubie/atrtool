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

