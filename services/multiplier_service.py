"""5x Multiplier service with Omega safety."""

current_multiplier = 1
total_presses = 0

class MultiplierService:
    @classmethod
    def apply(cls) -> Dict:
        global current_multiplier, total_presses
        if current_multiplier >= 1000000: return {"success": False}
        current_multiplier *= 5
        total_presses += 1
        return {"success": True, "new_multiplier": current_multiplier, "press_number": total_presses}