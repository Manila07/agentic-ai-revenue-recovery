from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentOut(BaseModel):
    id: str
    customer_id: str
    amount: float
    currency: str = "INR"
    method: str = "card"
    status: str
    failure_reason: Optional[str] = None
    failure_category: Optional[str] = None
    created_at: Optional[datetime] = None
    recovered: bool = False
    recovered_amount: float = 0.0
    recovery_probability: float = 0.0

    class Config:
        from_attributes = True

class PaymentSimulate(BaseModel):
    amount: float = Field(..., gt=0)
    failure_reason: Optional[str] = Field(None)
    customer_id: Optional[str] = Field(None)