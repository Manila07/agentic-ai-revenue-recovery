from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RecoveryAnalysis(BaseModel):
    payment_id: str
    recovery_probability: float
    risk_score: float
    recommended_action: str
    confidence: float
    explanation: str
    requires_human_approval: bool
    factors: dict = {}


class RecoveryExecuteRequest(BaseModel):
    strategy: str
    approved: bool = False


class RecoveryResponse(BaseModel):
    id: int
    payment_id: str
    strategy: str
    status: str
    recovery_probability: float
    risk_score: float
    explanation: str
    requires_human_approval: bool
    result: Optional[str] = None
    recovered_amount: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecoveryListResponse(BaseModel):
    recoveries: list[RecoveryResponse]
    total: int
