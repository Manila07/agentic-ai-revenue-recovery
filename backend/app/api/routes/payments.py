"""
Payments API — list, detail, simulate failed payments.
"""
import random
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# ---- VERIFY THESE TWO LINES against your repo ----
from app.database import get_db                 # where your DB session dependency lives
from app.models.payment import Payment          # where your Payment model lives
# --------------------------------------------------

# NOTE: no prefix here — router.py already mounts this under /api/payments
router = APIRouter(tags=["payments"])


def _serialize(p):
    return {
        "id": p.id,
        "merchant_id": p.merchant_id,
        "customer_id": p.customer_id,
        "amount": p.amount,
        "currency": p.currency,
        "status": p.status,
        "failure_reason": p.failure_reason,
        "failure_code": p.failure_code,
        "failure_category": p.failure_code,
        "payment_method": p.payment_method,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        "retry_count": p.retry_count,
        "customer_total_payments": p.customer_total_payments,
        "customer_successful_payments": p.customer_successful_payments,
        "customer_failed_payments": p.customer_failed_payments,
        "customer_success_rate": p.customer_success_rate,
        "customer_previous_retries": p.customer_previous_retries,
    }


@router.get("")
@router.get("/")
def list_payments(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    return {"payments": [_serialize(p) for p in payments]}


@router.get("/{payment_id}")
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail=f"Payment {payment_id} not found")
    return _serialize(payment)


@router.post("/simulate-failure")
def simulate_failure(amount: float = 500.0, db: Session = Depends(get_db)):
    templates = [
        ("Network timeout while processing payment", "NETWORK"),
        ("Customer balance below amount", "INSUFFICIENT_FUNDS"),
        ("Card has expired", "CARD_EXPIRED"),
        ("Bank declined the transaction", "BANK_DECLINE"),
        ("Payment gateway not responding", "GATEWAY_TIMEOUT"),
    ]
    reason, code = random.choice(templates)
    total = random.randint(3, 20)
    success = random.randint(0, total)

    payment = Payment(
        id=f"PAY_{secrets.token_hex(4).upper()}",
        merchant_id="merchant_test",
        customer_id=f"CUST_{random.randint(100000, 999999)}",
        amount=amount,
        currency="INR",
        status="failed",
        failure_reason=reason,
        failure_code=code,
        payment_method=random.choice(["card", "upi", "netbanking"]),
        created_at=datetime.utcnow() - timedelta(minutes=random.randint(1, 120)),
        updated_at=datetime.utcnow(),
        retry_count=random.randint(0, 2),
        customer_total_payments=total,
        customer_successful_payments=success,
        customer_failed_payments=total - success,
        customer_success_rate=round(success / total, 2),
        customer_previous_retries=random.randint(0, 2),
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return _serialize(payment)
