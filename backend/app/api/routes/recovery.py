from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.recovery_service import (
    analyze_payment_service,
    execute_recovery_service,
    get_recovery_history,
)

router = APIRouter()


@router.get("/")
def list_recoveries(db: Session = Depends(get_db)):
    from app.models.recovery import RecoveryAttempt
    attempts = (
        db.query(RecoveryAttempt)
        .order_by(RecoveryAttempt.created_at.desc())
        .limit(50)
        .all()
    )
    return {
        "recoveries": [
            {
                "id": a.id,
                "payment_id": a.payment_id,
                "strategy": a.strategy,
                "status": a.status,
                "recovered_amount": a.recovered_amount,
                "created_at": str(a.created_at) if a.created_at else None,
            }
            for a in attempts
        ]
    }


@router.post("/{payment_id}/analyze")
async def analyze(payment_id: str, db: Session = Depends(get_db)):
    try:
        return await analyze_payment_service(db, payment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{payment_id}/execute")
async def execute(payment_id: str, human_approved: bool = False, db: Session = Depends(get_db)):
    try:
        return await execute_recovery_service(db, payment_id, human_approved)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{payment_id}/history")
def history(payment_id: str, db: Session = Depends(get_db)):
    attempts = get_recovery_history(db, payment_id)
    return {
        "history": [
            {"id": a.id, "strategy": a.strategy, "status": a.status,
             "recovered_amount": a.recovered_amount,
             "created_at": str(a.created_at) if a.created_at else None}
            for a in attempts
        ]
    }
