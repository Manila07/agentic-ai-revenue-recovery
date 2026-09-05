from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/stats")
def payment_stats(db: Session = Depends(get_db)):
    from app.models.payment import Payment
    from sqlalchemy import func
    
    total = db.query(Payment).count()
    total_amount = db.query(func.sum(Payment.amount)).scalar() or 0
    avg_amount = db.query(func.avg(Payment.amount)).scalar() or 0
    
    return {
        "total_payments": total,
        "total_amount": round(total_amount, 2),
        "average_amount": round(avg_amount, 2),
    }

@router.get("/")
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
):
    from app.models.payment import Payment
    
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    
    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "payments": [
            {
                "id": p.id,
                "merchant_id": p.merchant_id,
                "customer_id": p.customer_id,
                "amount": p.amount,
                "currency": p.currency,
                "status": p.status,
                "failure_reason": p.failure_reason,
                "failure_code": p.failure_code,
                "payment_method": p.payment_method,
                "retry_count": p.retry_count,
                "customer_success_rate": p.customer_success_rate,
                "created_at": str(p.created_at) if p.created_at else None,
            }
            for p in payments
        ],
        "total": total,
    }

@router.get("/{payment_id}")
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    from app.models.payment import Payment
    
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return {"error": "Payment not found"}
    
    return {
        "id": payment.id,
        "merchant_id": payment.merchant_id,
        "customer_id": payment.customer_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "status": payment.status,
        "failure_reason": payment.failure_reason,
        "failure_code": payment.failure_code,
        "payment_method": payment.payment_method,
        "retry_count": payment.retry_count,
        "customer_total_payments": payment.customer_total_payments,
        "customer_successful_payments": payment.customer_successful_payments,
        "customer_failed_payments": payment.customer_failed_payments,
        "customer_success_rate": payment.customer_success_rate,
        "customer_previous_retries": payment.customer_previous_retries,
        "created_at": str(payment.created_at) if payment.created_at else None,
    }
