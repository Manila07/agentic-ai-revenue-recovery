from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.agent import AgentActionOut, AgentTimelineOut
from app.services.recovery_service import RecoveryService

router = APIRouter()

@router.get("/activity", response_model=List[AgentActionOut])
async def get_agent_activity(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return RecoveryService.get_agent_activity(db, limit=limit, offset=offset)

@router.get("/timeline/{payment_id}", response_model=AgentTimelineOut)
async def get_agent_timeline(payment_id: str, db: Session = Depends(get_db)):
    return RecoveryService.get_agent_timeline(db, payment_id)