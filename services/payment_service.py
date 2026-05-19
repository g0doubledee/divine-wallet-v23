"""Payment processing service."""

from typing import Dict, List

transactions = []

class PaymentService:
    @classmethod
    async def process_payment(cls, amount: float, merchant: str, rail: str) -> Dict:
        tx_id = f"TXN_{hash(str(amount) + merchant)}"
        transactions.insert(0, {"id": tx_id, "amount": amount, "merchant": merchant, "rail": rail, "status": "approved"})
        return {"success": True, "transaction_id": tx_id}