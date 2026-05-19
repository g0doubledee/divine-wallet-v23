
from core.ai_brainiac import Brainiac
result = Brainiac.execute_auto_deposit(amount_usd, source="Divine Wallet")
if not result["all_succeeded"]:
    logger.error("Brainiac failed to route funds!")