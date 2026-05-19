"""DUKPT (Derived Unique Key Per Transaction) - ANSI X9.24."""

import hashlib
import secrets
from typing import Tuple

class DUKPT:
    @staticmethod
    def derive_peks(bdk: bytes, ksn: bytes) -> bytes:
        return hashlib.sha256(bdk + ksn).digest()[:16]
    @staticmethod
    def generate_ksn(device_id: int, counter: int) -> bytes:
        return device_id.to_bytes(4, 'big') + counter.to_bytes(4, 'big') + b'\x00\x00'