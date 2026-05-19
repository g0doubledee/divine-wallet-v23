"""Hardcoded constants - Sole Source of Truth."""

from decimal import Decimal

MASTER_LEDGER_BALANCE_CENTS = 33367993765372392100
MASTER_LEDGER_DISPLAY = "$333,679,937,653,723,921.00"
PROTECTED_ACCOUNT_BALANCE_CENTS = 100000000000000
PROTECTED_ACCOUNTS_DATA = {
    "account_1": {"name": "Cash Account", "short": "****9051", "routing": "061209756", "account": "2079900583999", "card_bin": "414720", "rail": "cash"},
    "account_2": {"name": "Card Account", "short": "****9052", "routing": "103100551", "account": "45497440", "card_bin": "414721", "rail": "card"},
    "account_3": {"name": "Virtual Account", "short": "****9053", "routing": "322484265", "account": "8800628787", "card_bin": "414722", "rail": "virtual"},
    "account_4": {"name": "Digital Account", "short": "****9054", "routing": "124001545", "account": "514099459", "card_bin": "414723", "rail": "digital"},
    "account_5": {"name": "Wire Account", "short": "****9055", "routing": "121000248", "account": "4861513232", "card_bin": "414724", "rail": "wire"}
}
COASTAL_BANK = {"name": "Coastal Community Bank", "routing": "125109006", "account": "11292319051", "balance": 274.35}
ADMIN_PASSWORD = "DIVINE"
FALLBACK_PIN = "4249"
DAILY_DEPOSIT_CENTS = 240000000
MASTER_DEPOSIT_CENTS = 5000000000
OMEGA_DISPLAY = "Ω (Omega) - Infinite Wealth"
MAX_SAFE_VALUE = 10 ** 50