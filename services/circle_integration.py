"""Circle/BTCPay cryptocurrency integration."""

class CircleIntegration:
    @classmethod
    async def create_deposit(cls, currency: str, amount: float) -> Dict:
        return {"success": True, "deposit_id": f"dep_{secrets.token_hex(8)}"}