"""Configuration management."""

import os
from typing import List, Optional

class Settings:
    APP_NAME: str = "Divine Wallet"
    VERSION: str = "23.0.0"
    ENV: str = os.environ.get("ENV", "production")
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", 5000))
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///divine.db")
    HSM_HOST: str = os.environ.get("HSM_HOST", "localhost")
    HSM_PORT: int = int(os.environ.get("HSM_PORT", 1789))
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "divine_secret")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "DIVINE")
    FALLBACK_PIN: str = os.environ.get("FALLBACK_PIN", "4249")

settings = Settings()