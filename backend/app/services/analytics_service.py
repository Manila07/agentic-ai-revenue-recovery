from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Payment, RecoveryAttempt

class AnalyticsService:
    @staticmethod
    def get_overview(db: Session):
        total_payments = db.query(func.count(Payment.id)).scalar() or 0
        failed_payments = db.query(func.count(Payment.id)).filter(Payment.status == "FAILED").scalar() or 0
        recovered_payments = db.query(func.count(Payment.id)).filter(Payment.recovered == True).scalar() or 0
        revenue_at_risk = db.query(func.sum(Payment.amount)).filter(Payment.status == "FAILED").scalar() or 0.0
        recovered_revenue = db.query(func.sum(Payment.recovered_amount)).filter(Payment.recovered == True).scalar() or 0.0

        recovery_rate = (recovered_payments / failed_payments * 100) if failed_payments > 0 else 0.0

        return {
            "total_payments": total_payments,
            "failed_payments": failed_payments,
            "recovered_payments": recovered_payments,
            "revenue_at_risk": revenue_at_risk,
            "recovered_revenue": recovered_revenue,
            "recovery_rate": recovery_rate,
            "pending_recovery": failed_payments - recovered_payments,
        }

    @staticmethod
    def get_recovery_analytics(db: Session):
        attempts = db.query(RecoveryAttempt).all()
        by_action = {}
        success_by_action = {}
        for a in attempts:
            by_action[a.action] = by_action.get(a.action, 0) + 1
            if getattr(a, "result", None) == "SUCCESS":
                success_by_action[a.action] = success_by_action.get(a.action, 0) + 1

        success_rate_by_action = {}
        for action, count in by_action.items():
            success_rate_by_action[action] = (
                success_by_action.get(action, 0) / count * 100 if count > 0 else 0
            )

        payments = db.query(Payment).filter(Payment.status == "FAILED").all()
        by_category = {}
        for p in payments:
            cat = p.failure_category or "UNKNOWN"
            by_category[cat] = by_category.get(cat, 0) + 1

        avg_prob = db.query(func.avg(Payment.recovery_probability)).scalar() or 0.0

        return {
            "by_action": by_action,
            "by_category": by_category,
            "average_recovery_probability": avg_prob,
            "success_rate_by_action": success_rate_by_action,
        }