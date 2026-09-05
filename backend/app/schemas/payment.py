from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):
    id: str
    merchant_id: str
    customer_id: str
    amount: float
    currency: str = "INR"
    status: str
    failure_reason: str
    failure_code: str
    payment_method: str
    retry_count: int = 0


class PaymentResponse(PaymentBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    customer_total_payments: int = 0
    customer_successful_payments: int = 0
    customer_failed_payments: int = 0
    customer_success_rate: float = 0.0
    customer_previous_retries: int = 0

    class Config:
        from_attributes = True


class PaymentListResponse(BaseModel):
    payments: list[PaymentResponse]
    total: int
    page: int = 1
    per_page: int = 20
