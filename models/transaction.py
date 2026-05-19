"""Transaction data models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    id: str
    amount: float
    currency: str = "USD"
    merchant: str
    status: str
    created_at: datetime = datetime.now()