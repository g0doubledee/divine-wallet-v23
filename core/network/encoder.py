"""ISO 8583 binary encoder/decoder."""

class ISO8583Message:
    def __init__(self, mti: str = "0200"):
        self.mti, self.fields = mti, {}
    def set_field(self, num: int, value: str):
        self.fields[num] = value
    def get_field(self, num: int, default: str = "") -> str:
        return self.fields.get(num, default)
    def encode(self) -> bytes:
        result = self.mti.encode()
        result += b"\xC0\x00\x00\x00\x00\x00\x00\x00"
        for num, value in sorted(self.fields.items()):
            result += value.encode()
        return result