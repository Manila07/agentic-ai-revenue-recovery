"""
Analytics service — computes charts and metrics data.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.payment import Payment
from app.models.recovery import RecoveryAttempt


def get_analytics_overview(db: Session) -> dict:
    """Dashboard metrics for analytics page."""
    total_payments = db.query(Payment).count()
    total_amount = db.query(func.sum(Payment.amount)).scalar() or 0
    total_recovered = db.query(
        func.sum(RecoveryAttempt.recovered_amount)
    ).filter(RecoveryAttempt.status == "success").scalar() or 0
    recovery_attempts = db.query(RecoveryAttempt).count()
    successful_recoveries = db.query(
        RecoveryAttempt
    ).filter(RecoveryAttempt.status == "success").count()

    return {
        "total_payments": total_payments,
        "total_at_risk_amount": round(total_amount, 2),
        "total_recovered_amount": round(total_recovered, 2),
        "recovery_rate": round(
            (successful_recoveries / recovery_attempts * 100) if recovery_attempts > 0 else 0,
            1
        ),
        "total_recovery_attempts": recovery_attempts,
        "successful_recoveries": successful_recoveries,
        "pending_human_review": db.query(
            RecoveryAttempt
        ).filter(
            RecoveryAttempt.status == "pending_approval"
        ).count(),
    }


def get_failure_reasons_chart(db: Session) -> list:
    """Failure reasons breakdown for pie/bar chart."""
    results = (
        db.query(Payment.failure_reason, func.count(Payment.id))
        .group_by(Payment.failure_reason)
        .all()
    )
    return [{"reason": r[0], "count": r[1]} for r in results]


def get_payment_methods_chart(db: Session) -> list:
    """Payment methods breakdown."""
    results = (
        db.query(Payment.payment_method, func.count(Payment.id))
        .group_by(Payment.payment_method)
        .all()
    )
    return [{"method": r[0], "count": r[1]} for r in results]


def get_amount_distribution(db: Session) -> list:
    """Payment amount distribution by ranges."""
    ranges = [
        (0, 500, "₹0-500"),
        (500, 2000, "₹500-2K"),
        (2000, 10000, "₹2K-10K"),
        (10000, 50000, "₹10K-50K"),
        (50000, float("inf"), "₹50K+"),
    ]
    result = []
    for low, high, label in ranges:
        count = db.query(Payment).filter(
            Payment.amount >= low,
            Payment.amount < high
        ).count()
        result.append({"range": label, "count": count})
    return result


def get_revenue_by_strategy(db: Session) -> list:
    """Recovered revenue grouped by strategy."""
    results = (
        db.query(
            RecoveryAttempt.strategy,
            func.count(RecoveryAttempt.id),
            func.sum(RecoveryAttempt.recovered_amount),
        )
        .filter(RecoveryAttempt.status == "success")
        .group_by(RecoveryAttempt.strategy)
        .all()
    )
    return [
        {
            "strategy": r[0],
            "attempts": r[1],
            "recovered": round(r[2] or 0, 2),
        }
        for r in results
    ]


def get_recovery_timeline(db: Session, days: int = 7) -> list:
    """Recovery attempts over time for line chart."""
    start_date = datetime.utcnow() - timedelta(days=days)
    results = (
        db.query(
            func.date(RecoveryAttempt.created_at).label("date"),
            func.count(RecoveryAttempt.id),
            func.sum(
                case(
                    (RecoveryAttempt.status == "success", RecoveryAttempt.recovered_amount),
                    else_=0,
                )
            ),
        )
        .filter(RecoveryAttempt.created_at >= start_date)
        .group_by(func.date(RecoveryAttempt.created_at))
        .all()
    )
    return [
        {"date": str(r[0]), "attempts": r[1], "recovered": round(r[2] or 0, 2)}
        for r in results
    ]


def get_agent_activity(db: Session, limit: int = 50) -> list:
    """Recent agent decisions and actions."""
    attempts = (
        db.query(RecoveryAttempt)
        .order_by(RecoveryAttempt.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": a.id,
            "payment_id": a.payment_id,
            "strategy": a.strategy,
            "status": a.status,
            "recovery_probability": a.recovery_probability,
            "risk_score": a.risk_score,
            "explanation": a.explanation,
            "recovered_amount": a.recovered_amount,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in attempts
    ]
