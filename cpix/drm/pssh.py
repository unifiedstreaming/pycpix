"""
PSSH box functionality
"""
from construct.core import Prefixed, Struct, Const, Int8ub, Int24ub, Int32ub, \
    Bytes, GreedyBytes, PrefixedArray, Default, If, this


PSSH_STRUCT = Prefixed(
    Int32ub,
    Struct(
        "type" / Const(b"pssh"),
        "version" / Default(Int8ub, 0),
        "flags" / Const(0, Int24ub),
        "system_id" / Bytes(16),
        "key_ids" / If(this.version == 1, PrefixedArray(Int32ub, Bytes(16))),
        "data" / Prefixed(Int32ub, GreedyBytes)
    ),
    includelength=True
)


class PSSH(object):
    """
    Base PSSH object
    """

    def __init__(self,
                 system_id,
                 version=0,
                 key_ids=None,
                 data=None):
        self._system_id = None
        self._version = 0
        self._key_ids = None
        self.data = None


    # properties
    @property
    def system_id(self):
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        # system ID must be a UUID
        if isinstance(system_id, str):
            self._system_id = uuid.UUID(system_id)
        elif isinstance(system_id, uuid.UUID):
            self._system_id = system_id
        else:
            raise TypeError("system ID must be a UUID")

    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, version):
