from pydantic import BaseModel
from typing import Dict, Any

class AnalyticsOverviewOut(BaseModel):
    total_payments: int
    failed_payments: int
    recovered_payments: int
    revenue_at_risk: float
    recovered_revenue: float
    recovery_rate: float
    pending_recovery: int

class RecoveryAnalyticsOut(BaseModel):
    by_action: Dict[str, int]
    by_category: Dict[str, int]
    average_recovery_probability: float
    success_rate_by_action: Dict[str, float]