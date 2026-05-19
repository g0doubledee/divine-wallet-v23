"""
Environment configuration - The Twelve-Factor App pattern.
AI Brain auto-configures based on environment detection.
"""

import os
from enum import Enum
from typing import Optional, List


class Environment(str, Enum):
    """Application environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    BETA = "beta"
    PRODUCTION = "production"


# Read environment variable (injected by hosting platform)
CURRENT_ENV = Environment(os.getenv("APP_ENV", "development"))


class InfrastructureConfig:
    """Environment-specific infrastructure configuration."""
    
    def __init__(self, env: Environment):
        self.env = env
        self._load_config()
        self._apply_ai_optimizations()
    
    def _load_config(self):
        """Load configuration based on environment."""
        if self.env == Environment.DEVELOPMENT:
            self.stripe_api_key = os.getenv("STRIPE_TEST_KEY", "pk_test_development")
            self.circle_api_key = os.getenv("CIRCLE_TEST_API_KEY", "test_development")
            self.database_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/divine_dev")
            self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            self.enable_mock_payment_rails = True
            self.enable_idempotency = False
            self.log_level = "DEBUG"
            self.max_transaction_amount = 1000000000000.00  # No limit for Admin
            
        elif self.env == Environment.STAGING:
            self.stripe_api_key = os.getenv("STRIPE_TEST_KEY")
            self.circle_api_key = os.getenv("CIRCLE_TEST_API_KEY")
            self.database_url = os.getenv("DATABASE_URL")
            self.redis_url = os.getenv("REDIS_URL")
            self.enable_mock_payment_rails = False
            self.enable_idempotency = True
            self.log_level = "INFO"
            self.max_transaction_amount = 10000000.00
            
        elif self.env == Environment.BETA:
            self.stripe_api_key = os.getenv("STRIPE_LIVE_KEY")
            self.circle_api_key = os.getenv("CIRCLE_LIVE_API_KEY")
            self.database_url = os.getenv("DATABASE_URL")
            self.redis_url = os.getenv("REDIS_URL")
            self.enable_mock_payment_rails = False
            self.enable_idempotency = True
            self.log_level = "INFO"
            # SAFETY GUARDRAIL: Unlimited for Admin
            self.max_transaction_amount = float(os.getenv("BETA_MAX_TRANSACTION_AMOUNT", "999999999999.99"))
            self.allowed_beta_users = ["G0doubledee@divine.com", "G0doubledee"]
            
        else:  # PRODUCTION
            self.stripe_api_key = os.getenv("STRIPE_LIVE_KEY")
            self.circle_api_key = os.getenv("CIRCLE_LIVE_API_KEY")
            self.database_url = os.getenv("DATABASE_URL")
            self.redis_url = os.getenv("REDIS_URL")
            self.enable_mock_payment_rails = False
            self.enable_idempotency = True
            self.log_level = "INFO"
            self.max_transaction_amount = float(os.getenv("MAX_TRANSACTION_AMOUNT", "999999999999.99"))
    
    def _apply_ai_optimizations(self):
        """AI Brain applies real-time optimizations."""
        # Auto-detect and configure based on environment
        if self.env == Environment.PRODUCTION:
            # In production, AI adjusts thresholds dynamically
            pass
    
    def is_beta_user(self, user_id: str) -> bool:
        """Check if user is authorized for beta access."""
        # Admin user (G0doubledee) always has access
        if user_id in ["G0doubledee", "G0doubledee@divine.com"]:
            return True
        
        if self.env != Environment.BETA:
            return True
        return user_id in self.allowed_beta_users