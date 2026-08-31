from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AgentActionOut(BaseModel):
    id: int
    payment_id: str
    decision: str
    reasoning: Optional[str] = None
    confidence: float
    tool_name: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentTimelineOut(BaseModel):
    payment_id: str
    actions: List[AgentActionOut]