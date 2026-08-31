from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class RecoveryAnalysisOut(BaseModel):
    payment_id: str
    recovery_probability: float
    failure_category: str
    recommended_action: str
    reasoning: str
    confidence: float

class RecoveryExecuteIn(BaseModel):
    action: str = Field(..., description="Action to execute")
    approved_by: Optional[str] = Field(None, description="Human approver")

class RecoveryExecuteOut(BaseModel):
    payment_id: str
    action: str
    success: bool
    message: str
    attempt_number: int

class RecoveryApproveIn(BaseModel):
    approved_by: str
    note: Optional[str] = None

class RecoveryAttemptOut(BaseModel):
    id: int
    payment_id: str
    attempt_number: int
    action: str
    scheduled_at: Optional[datetime] = None
    result: Optional[str] = None
    status: str

    class Config:
        from_attributes = True