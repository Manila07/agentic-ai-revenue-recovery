from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.payment import Payment
from app.schemas.payment import PaymentResponse, PaymentListResponse


def get_payments(
    db: Session,
    status: str = None,
    failure_reason: str = None,
    page: int = 1,
    per_page: int = 20,
) -> PaymentListResponse:
    """Get paginated list of payments with optional filters."""
    query = db.query(Payment)

    if status:
        query = query.filter(Payment.status == status)
    if failure_reason:
        query = query.filter(Payment.failure_reason == failure_reason)

    total = query.count()
    payments = (
        query.order_by(desc(Payment.created_at))
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return PaymentListResponse(
        payments=[PaymentResponse.model_validate(p) for p in payments],
        total=total,
        page=page,
        per_page=per_page,
    )


def get_payment(db: Session, payment_id: str) -> Payment | None:
    return db.query(Payment).filter(Payment.id == payment_id).first()


def update_payment_status(db: Session, payment_id: str, status: str) -> Payment | None:
    payment = get_payment(db, payment_id)
    if payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
    return payment


def get_payment_stats(db: Session) -> dict:
    """Aggregate stats for the dashboard."""
    total = db.query(Payment).count()
    failed = db.query(Payment).filter(Payment.status == "failed").count()
    recovered = db.query(Payment).filter(Payment.status == "recovered").count()

    total_revenue = db.query(func.sum(Payment.amount)).scalar() or 0
    recovered_revenue = (
        db.query(func.sum(Payment.amount))
        .filter(Payment.status == "recovered")
        .scalar()
        or 0
    )

    # By failure reason
    reasons = (
        db.query(Payment.failure_reason, func.count(Payment.id))
        .group_by(Payment.failure_reason)
        .all()
    )

    # By payment method
    methods = (
        db.query(Payment.payment_method, func.count(Payment.id))
        .group_by(Payment.payment_method)
        .all()
    )

    return {
        "total_payments": total,
        "failed_payments": failed,
        "recovered_payments": recovered,
        "total_revenue": round(total_revenue, 2),
        "recovered_revenue": round(recovered_revenue, 2),
        "recovery_rate": round(recovered / max(total, 1) * 100, 1),
        "failure_reasons": {r: c for r, c in reasons},
        "payment_methods": {m: c for m, c in methods},
    }
