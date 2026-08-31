from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

from app.database.database import get_db
from app.schemas.payment import PaymentOut, PaymentSimulate
from app.services.payment_service import PaymentService
from payments.simulator.payment_simulator import PaymentSimulator

router = APIRouter()

@router.get("", response_model=List[PaymentOut])
async def list_payments(status: Optional[str] = None, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    return PaymentService.get_payments(db, status=status, limit=limit, offset=offset)

@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.post("/simulate-failure", response_model=PaymentOut)
async def simulate_failure(data: PaymentSimulate, db: Session = Depends(get_db)):
    simulator = PaymentSimulator()
    payment_data = simulator.generate_failed_transaction(
        amount=data.amount,
        failure_reason=data.failure_reason,
        customer_id=data.customer_id,
    )
    payment = PaymentService.create_payment(db, payment_data)

    # Trigger recovery workflow asynchronously (broadcasts events via WebSocket)
    from app.services.recovery_service import RecoveryService
    asyncio.create_task(RecoveryService.trigger_recovery_workflow(db, payment.id))

    return payment