from typing import Self


class GatewaySingleton:
    _instance: Self | None = None

    def __init__(self):
        if GatewaySingleton._instance is None:
            GatewaySingleton._instance = self
        else:
            raise RuntimeError("GatewaySingleton already initialized")

    @classmethod
    def get_instance(cls):
        if GatewaySingleton._instance is not None:
            return GatewaySingleton._instance
        else:
            raise RuntimeError("Attempted to access instance before initialization")
