from core.ai_brainiac import Brainiac
@app.post("/v1/payment")
async def make_payment(...):
    return Brainiac.guarantee_transaction(amount, merchant, rail) 
    @app.get("/v1/brainiac/status")
async def brainiac_status():
    return Brainiac.get_status()

@app.get("/v1/brainiac/constitution")
async def brainiac_constitution():
    return {"constitution": Brainiac.get_constitution()}