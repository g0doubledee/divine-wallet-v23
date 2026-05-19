from core.ai_brainiac import Brainiac
@app.post("/v1/payment")
async def make_payment(...):
    return Brainiac.guarantee_transaction(amount, merchant, rail)