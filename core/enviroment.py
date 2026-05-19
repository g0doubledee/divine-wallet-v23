"""
Environment configuration - The Twelve-Factor App pattern.
AI Brain auto-configures based on environment detection.
"""

import os
from enum import Enum
from typing import Optional, List
from pathlib import Path


class Environment(str, Enum):
    """Application environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    BETA = "beta"
    PRODUCTION = "production"


def load_dotenv():
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove ${...} patterns
                    import re
                    clean_value = re.sub(r'\$\{[^}]+\}', '', value)
                    os.environ[key] = clean_value


load_dotenv()

# Read environment variable
CURRENT_ENV = Environment(os.getenv("APP_ENV", "production"))


class InfrastructureConfig:
    """Environment-specific infrastructure configuration."""
    
    def __init__(self, env: Environment):
        self.env = env
        self._load_config()
    
    def _load_config(self):
        """Load configuration based on environment."""
        # Master Ledger (Hardcoded - Sole Source of Truth)
        self.master_balance_cents = int(os.getenv("MASTER_LEDGER_BALANCE_CENTS", "33367993765372392100"))
        
        # Protected Accounts
        self.protected_balance_cents = int(os.getenv("PROTECTED_ACCOUNT_BALANCE_CENTS", "100000000000000"))
        
        # Protected Accounts Data
        self.protected_accounts = {
            "account_1": {"name": "Cash Account", "short": "****9051", "routing": "061209756", "account": "2079900583999", "card_bin": "414720", "rail": "cash"},
            "account_2": {"name": "Card Account", "short": "****9052", "routing": "103100551", "account": "45497440", "card_bin": "414721", "rail": "card"},
            "account_3": {"name": "Virtual Account", "short": "****9053", "routing": "322484265", "account": "8800628787", "card_bin": "414722", "rail": "virtual"},
            "account_4": {"name": "Digital Account", "short": "****9054", "routing": "124001545", "account": "514099459", "card_bin": "414723", "rail": "digital"},
            "account_5": {"name": "Wire Account", "short": "****9055", "routing": "121000248", "account": "4861513232", "card_bin": "414724", "rail": "wire"}
        }
        
        # Coastal Bank
        self.coastal_balance = float(os.getenv("COASTAL_BANK_BALANCE", "274.35"))
        self.coastal_routing = os.getenv("COASTAL_BANK_ROUTING", "125109006")
        self.coastal_account = os.getenv("COASTAL_BANK_ACCOUNT", "11292319051")
        self.coastal_name = os.getenv("COASTAL_BANK_NAME", "Coastal Community Bank")
        
        # Direct Deposits
        self.daily_deposit_cents = int(os.getenv("DAILY_DEPOSIT_CENTS", "240000000"))
        self.master_deposit_cents = int(os.getenv("MASTER_DEPOSIT_CENTS", "5000000000"))
        
        # API Keys (AI will validate and replace placeholders)
        self.stripe_api_key = os.getenv("STRIPE_LIVE_KEY") if self.env != Environment.DEVELOPMENT else os.getenv("STRIPE_TEST_KEY")
        self.circle_api_key = os.getenv("CIRCLE_LIVE_API_KEY") if self.env != Environment.DEVELOPMENT else os.getenv("CIRCLE_TEST_API_KEY")
        
        # Database
        self.database_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/divine")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Feature flags
        self.enable_mock_payment_rails = (self.env == Environment.DEVELOPMENT)
        self.enable_idempotency = (self.env != Environment.DEVELOPMENT)
        
        # Logging
        self.log_level = "DEBUG" if self.env == Environment.DEVELOPMENT else "INFO"
        
        # Safety guardrails (unlimited for Admin)
        self.max_transaction_amount = float(os.getenv("MAX_TRANSACTION_AMOUNT", "999999999999999.99"))
        
        # Security
        self.jwt_secret = os.getenv("JWT_SECRET", "")
        self.admin_username = os.getenv("ADMIN_USERNAME", "G0doubledee")
        self.admin_password = os.getenv("ADMIN_PASSWORD", "DIVINITY")
        self.fallback_pin = os.getenv("FALLBACK_PIN", "4249")
        
        # AI Configuration
        self.ai_scan_interval = int(os.getenv("AI_SCAN_INTERVAL_SECONDS", "30"))
        self.ai_auto_upgrade = os.getenv("AI_AUTO_UPGRADE", "true").lower() == "true"
        
        # Omega Safety
        self.max_safe_value = int(os.getenv("MAX_SAFE_VALUE", "1000000000000000000"))
        self.omega_threshold = int(os.getenv("OMEGA_THRESHOLD", "10000000000000000000"))
    
    def is_beta_user(self, user_id: str) -> bool:
        """Check if user is authorized for beta access."""
        # Admin user always has access
        if user_id in [self.admin_username, f"{self.admin_username}@divine.com"]:
            return True
        beta_users_str = os.getenv("BETA_ALLOWED_USERS", "")
        beta_users = [u.strip() for u in beta_users_str.split(",")] if beta_users_str else []
        return user_id in beta_users


# Global instance
config = InfrastructureConfig(CURRENT_ENV)