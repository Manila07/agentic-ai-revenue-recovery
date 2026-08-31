from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.recovery import RecoveryAnalysisOut, RecoveryExecuteIn, RecoveryExecuteOut, RecoveryApproveIn
from app.services.recovery_service import RecoveryService
from app.services.payment_service import PaymentService

router = APIRouter()

@router.post("/analyze/{payment_id}", response_model=RecoveryAnalysisOut)
async def analyze_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return RecoveryService.analyze_payment(db, payment)

@router.post("/execute/{payment_id}", response_model=RecoveryExecuteOut)
async def execute_recovery(
    payment_id: str,
    data: RecoveryExecuteIn,
    db: Session = Depends(get_db),
):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return RecoveryService.execute_recovery(db, payment, data.action, data.approved_by)

@router.post("/approve/{payment_id}", response_model=RecoveryExecuteOut)
async def approve_recovery(
    payment_id: str,
    data: RecoveryApproveIn,
    db: Session = Depends(get_db),
):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return RecoveryService.approve_recovery(db, payment, data.approved_by)