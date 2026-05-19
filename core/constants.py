"""
Hardcoded constants - Sole Source of Truth.
These values are the foundation of Divine Wallet.
"""

from decimal import Decimal, getcontext

getcontext().prec = 100

# ==================== OMEGA SAFETY SYSTEM ====================
OMEGA_DISPLAY = "Ω (Omega) - Infinite Wealth"
MAX_SAFE_VALUE = 10 ** 50

# ==================== MASTER LEDGER (Sole Source of Truth) ====================
MASTER_LEDGER_BALANCE_CENTS = 33367993765372392100
MASTER_LEDGER_BALANCE_USD = Decimal("333679937653723921.00")
MASTER_LEDGER_DISPLAY = "$333,679,937,653,723,921.00"

# ==================== 5 PROTECTED ACCOUNTS ====================
PROTECTED_ACCOUNT_BALANCE_CENTS = 100000000000000
PROTECTED_ACCOUNT_BALANCE_USD = Decimal("1000000000000.00")
PROTECTED_ACCOUNT_DISPLAY = "$1,000,000,000,000.00"

# ==================== COASTAL COMMUNITY BANK ====================
COASTAL_BANK_NAME = "Coastal Community Bank"
COASTAL_BANK_ROUTING = "125109006"
COASTAL_BANK_ACCOUNT = "11292319051"
COASTAL_BANK_ADDRESS = "5415 Evergreen Way, Everett, WA 98203"
COASTAL_BANK_INITIAL_BALANCE = ?

# ==================== DIRECT DEPOSIT SCHEDULE ====================
DAILY_DEPOSIT_AMOUNT_CENTS = 240000000  # $2.4M
DAILY_DEPOSIT_AMOUNT_USD = Decimal("2400000.00")
MASTER_DEPOSIT_AMOUNT_CENTS = 5000000000  # $50M
MASTER_DEPOSIT_AMOUNT_USD = Decimal("50000000.00")

# Deposit schedule: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
DEPOSIT_SCHEDULE = {
    0: "account_1",  # Monday
    1: "account_2",  # Tuesday
    2: "account_3",  # Wednesday
    3: "account_4",  # Thursday
    4: "account_5"   # Friday
}

# ==================== CARD NETWORK BINS ====================
CARD_BINS = {
    "account_1": "414720",
    "account_2": "414721",
    "account_3": "414722",
    "account_4": "414723",
    "account_5": "414724"
}

# ==================== ISO 8583 CONSTANTS ====================
ISO8583_RESPONSE_CODES = {
    "00": "Approved",
    "01": "Refer to card issuer",
    "05": "Do not honor",
    "51": "Insufficient funds",
    "54": "Expired card",
    "91": "Issuer unavailable"
}

# ==================== MULTIPLIER CONSTANTS ====================
INITIAL_MULTIPLIER = 1
MULTIPLIER_FACTOR = 5
MAX_SAFE_MULTIPLIER = 1000000

# ==================== SECURITY CONSTANTS ====================
ADMIN_USERNAME = "G0doubledee"
ADMIN_PASSWORD = "DIVINITY"
FALLBACK_PIN = "4249"
JWT_EXPIRATION_HOURS = 24
JWT_ALGORITHM = "HS256"

# ==================== AI BRAIN CONSTANTS ====================
AI_MODEL_VERSION = "6.0.0"
AI_CONFIDENCE_THRESHOLD = 0.9999
AI_LEARNING_RATE = 0.01
AI_SCAN_INTERVAL_SECONDS = 30

# ==================== OMEGA SAFETY FUNCTIONS ====================
def omega_safe_display(value):
    """Convert astronomically large numbers to Omega display."""
    try:
        if value > MAX_SAFE_VALUE:
            return OMEGA_DISPLAY
        return f"${value:,.2f}"
    except (OverflowError, ValueError, TypeError):
        return OMEGA_DISPLAY

def format_with_omega(cents):
    """Format cents with Omega safety."""
    try:
        if cents > MAX_SAFE_VALUE * 100 or len(str(cents)) > 50:
            return OMEGA_DISPLAY
        return f"${cents/100:,.2f}"
    except (OverflowError, ValueError):
        return OMEGA_DISPLAY