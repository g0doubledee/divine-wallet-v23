"""
5x Multiplier Service - Compounding balance multiplier.
Affects ALL accounts including Master Ledger and 5 Protected Accounts.
"""

import logging
from typing import Dict, Any
from decimal import Decimal

from core.constants import (
    MASTER_LEDGER_BALANCE_CENTS, PROTECTED_ACCOUNT_BALANCE_CENTS,
    MULTIPLIER_FACTOR, MAX_SAFE_MULTIPLIER, format_with_omega
)
from core.environment import config

logger = logging.getLogger("divine.services.multiplier")


class MultiplierService:
    """Manages the compounding 5x multiplier for all accounts."""
    
    _current_multiplier = 1
    _total_presses = 0
    _master_balance_cents = MASTER_LEDGER_BALANCE_CENTS
    _protected_balances = {
        "account_1": PROTECTED_ACCOUNT_BALANCE_CENTS,
        "account_2": PROTECTED_ACCOUNT_BALANCE_CENTS,
        "account_3": PROTECTED_ACCOUNT_BALANCE_CENTS,
        "account_4": PROTECTED_ACCOUNT_BALANCE_CENTS,
        "account_5": PROTECTED_ACCOUNT_BALANCE_CENTS * 10
    }
    _coastal_balance = config.coastal_balance
    
    @classmethod
    def initialize(cls):
        """Initialize the multiplier service."""
        logger.info(f"Multiplier Service initialized - Current: {cls._current_multiplier}x")
    
    @classmethod
    def get_current_multiplier(cls) -> int:
        return cls._current_multiplier
    
    @classmethod
    def get_master_balance(cls) -> float:
        return cls._master_balance_cents / 100
    
    @classmethod
    def get_master_balance_display(cls) -> str:
        return format_with_omega(cls._master_balance_cents)
    
    @classmethod
    def get_accounts_status(cls) -> Dict:
        """Get status of all protected accounts."""
        accounts = []
        for acc_id, balance in cls._protected_balances.items():
            acc_info = config.protected_accounts.get(acc_id, {})
            accounts.append({
                "id": acc_id,
                "name": acc_info.get("name", acc_id),
                "short": acc_info.get("short", "****0000"),
                "balance": format_with_omega(balance),
                "card_bin": acc_info.get("card_bin", "000000"),
                "rail": acc_info.get("rail", "unknown")
            })
        
        accounts.append({
            "id": "master",
            "name": "Master Ledger",
            "short": "****9050",
            "balance": format_with_omega(cls._master_balance_cents),
            "is_sole_source": True
        })
        
        return {"accounts": accounts, "count": len(accounts)}
    
    @classmethod
    def apply_multiplier(cls) -> Dict:
        """Apply 5x multiplier to ALL accounts (compounding)."""
        if cls._current_multiplier >= MAX_SAFE_MULTIPLIER:
            return {"success": False, "error": "Maximum multiplier reached (Omega safety)"}
        
        old_multiplier = cls._current_multiplier
        cls._current_multiplier *= MULTIPLIER_FACTOR
        cls._total_presses += 1
        
        # Multiply all balances
        cls._master_balance_cents *= MULTIPLIER_FACTOR
        for acc_id in cls._protected_balances:
            cls._protected_balances[acc_id] *= MULTIPLIER_FACTOR
        
        logger.info(f"Multiplier applied: {old_multiplier}x → {cls._current_multiplier}x")
        
        return {
            "success": True,
            "press_number": cls._total_presses,
            "old_multiplier": old_multiplier,
            "new_multiplier": cls._current_multiplier,
            "new_balance": format_with_omega(cls._master_balance_cents),
            "message": f"Balance multiplied! Now at {cls._current_multiplier}x"
        }
    
    @classmethod
    def deduct_from_protected(cls, account_id: str, amount_cents: int) -> bool:
        """Deduct amount from protected account."""
        if account_id in cls._protected_balances:
            if cls._protected_balances[account_id] >= amount_cents:
                cls._protected_balances[account_id] -= amount_cents
                cls._master_balance_cents -= amount_cents
                return True
        return False
    
    @classmethod
    def get_coastal_balance(cls) -> float:
        return cls._coastal_balance