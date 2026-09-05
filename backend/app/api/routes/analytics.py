from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db

router = APIRouter()

@router.get("/overview")
def analytics_overview(db: Session = Depends(get_db)):
    from app.models.payment import Payment
    from app.models.recovery import RecoveryAttempt

    total = db.query(Payment).count()
    total_amount = db.query(func.sum(Payment.amount)).scalar() or 0
    recovered = db.query(func.sum(RecoveryAttempt.recovered_amount)).filter(
        RecoveryAttempt.status == "success"
    ).scalar() or 0
    attempts = db.query(RecoveryAttempt).count()
    successful = db.query(RecoveryAttempt).filter(RecoveryAttempt.status == "success").count()

    return {
        "total_payments": total,
        "total_at_risk_amount": round(total_amount, 2),
        "total_recovered_amount": round(recovered, 2),
        "recovery_rate": round((successful / attempts * 100) if attempts > 0 else 0, 1),
        "total_recovery_attempts": attempts,
        "pending_human_review": db.query(RecoveryAttempt).filter(
            RecoveryAttempt.status == "pending_approval"
        ).count(),
    }

@router.get("/failure-reasons")
def failure_reasons(db: Session = Depends(get_db)):
    from app.models.payment import Payment
    results = db.query(Payment.failure_reason, func.count(Payment.id)).group_by(Payment.failure_reason).all()
    return [{"reason": r[0], "count": r[1]} for r in results]

@router.get("/payment-methods")
def payment_methods(db: Session = Depends(get_db)):
    from app.models.payment import Payment
    results = db.query(Payment.payment_method, func.count(Payment.id)).group_by(Payment.payment_method).all()
    return [{"method": r[0], "count": r[1]} for r in results]

@router.get("/amount-distribution")
def amount_distribution(db: Session = Depends(get_db)):
    from app.models.payment import Payment
    ranges = [
        (0, 500, "₹0-500"), (500, 2000, "₹500-2K"), 
        (2000, 10000, "₹2K-10K"), (10000, 50000, "₹10K-50K"), 
        (50000, 999999, "₹50K+")
    ]
    return [
        {"range": label, "count": db.query(Payment).filter(
            Payment.amount >= low, Payment.amount < high
        ).count()} 
        for low, high, label in ranges
    ]

@router.get("/revenue-by-strategy")
def revenue_by_strategy(db: Session = Depends(get_db)):
    from app.models.recovery import RecoveryAttempt
    results = db.query(
        RecoveryAttempt.strategy,
        func.count(RecoveryAttempt.id),
        func.sum(RecoveryAttempt.recovered_amount)
    ).group_by(RecoveryAttempt.strategy).all()
    return [{"strategy": r[0], "count": r[1], "recovered": round(r[2] or 0, 2)} for r in results]

@router.get("/agent-activity")
def agent_activity(db: Session = Depends(get_db)):
    from app.models.recovery import RecoveryAttempt
    attempts = db.query(RecoveryAttempt).order_by(RecoveryAttempt.created_at.desc()).limit(20).all()
    return [
        {
            "id": a.id,
            "payment_id": a.payment_id,
            "strategy": a.strategy,
            "status": a.status,
            "recovery_probability": a.recovery_probability,
            "created_at": str(a.created_at) if a.created_at else None,
        }
        for a in attempts
    ]
