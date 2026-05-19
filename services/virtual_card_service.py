"""Virtual card generation service."""

import secrets

class VirtualCardService:
    @classmethod
    def generate_card(cls, name: str) -> Dict:
        def luhn(base: str) -> str:
            digits = [int(d) for d in base]
            for i in range(len(digits)-2, -1, -2):
                d = digits[i] * 2
                digits[i] = d - 9 if d > 9 else d
            checksum = (10 - (sum(digits) % 10)) % 10
            return base + str(checksum)
        card_base = "414722" + ''.join([str(secrets.randbelow(10)) for _ in range(9)])
        card_number = luhn(card_base)
        return {"card_number": ' '.join([card_number[i:i+4] for i in range(0, 16, 4)]), "cvv": f"{secrets.randbelow(900)+100}"}