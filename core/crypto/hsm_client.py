"""Hardware Security Module client."""

import logging
from typing import Optional

logger = logging.getLogger("divine.crypto.hsm")

class HardwareSecurityModule:
    def __init__(self, host: str, port: int):
        self.host, self.port, self._connected = host, port, False
    async def connect(self) -> bool:
        self._connected = True
        return True
    async def disconnect(self):
        self._connected = False
    async def generate_key(self, key_type: str) -> str:
        return f"hsm_key_{key_type}"

class HardwareSecurityModulePool:
    _instances = {}
    @classmethod
    async def connect_hsm_clusters(cls, host: str, port: int):
        hsm = HardwareSecurityModule(host, port)
        await hsm.connect()
        cls._instances["primary"] = hsm
    @classmethod
    async def disconnect_all(cls):
        for hsm in cls._instances.values():
            await hsm.disconnect()
        cls._instances.clear()