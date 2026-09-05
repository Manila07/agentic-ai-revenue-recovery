from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db

router = APIRouter()

@router.get("/activity")
def agent_activity(db: Session = Depends(get_db)):
    """Recent agent decisions for the activity feed."""
    from app.models.recovery import RecoveryAttempt
    attempts = db.query(RecoveryAttempt).order_by(
        RecoveryAttempt.created_at.desc()
    ).limit(20).all()
    return {
        "activities": [
            {
                "id": a.id,
                "payment_id": a.payment_id,
                "strategy": a.strategy,
                "status": a.status,
                "recovery_probability": a.recovery_probability,
                "explanation": a.explanation,
                "recovered_amount": a.recovered_amount,
                "created_at": str(a.created_at) if a.created_at else None,
            }
            for a in attempts
        ]
    }

@router.post("/batch-recovery")
def batch_recovery(db: Session = Depends(get_db)):
    """Run recovery on all unprocessed failed payments."""
    from app.models.payment import Payment
    from app.models.recovery import RecoveryAttempt
    from app.services.recovery_engine import analyze_payment, execute_recovery

    # Get payments that haven't been attempted yet
    attempted_ids = db.query(RecoveryAttempt.payment_id).distinct().subquery()
    pending = db.query(Payment).filter(
        Payment.status == "failed",
        ~Payment.id.in_(db.query(attempted_ids.c.payment_id))
    ).limit(10).all()  # Process 10 at a time

    results = []
    for payment in pending:
        try:
            analysis = analyze_payment(db, payment.id)
            execution = execute_recovery(db, payment.id)
            results.append({
                "payment_id": payment.id,
                "amount": payment.amount,
                "strategy": analysis.get("selected_strategy", {}).get("name", "Unknown"),
                "probability": analysis.get("recovery_probability", 0),
                "success": execution.get("success", False),
                "recovered": execution.get("recovered_amount", 0),
            })
        except Exception as e:
            results.append({
                "payment_id": payment.id,
                "error": str(e),
            })

    total_recovered = sum(r.get("recovered", 0) for r in results)
    successful = sum(1 for r in results if r.get("success"))

    return {
        "processed": len(results),
        "successful": successful,
        "total_recovered": round(total_recovered, 2),
        "results": results,
    }

@router.get("/stats")
def agent_stats(db: Session = Depends(get_db)):
    """Agent performance stats."""
    from app.models.recovery import RecoveryAttempt
    
    total = db.query(RecoveryAttempt).count()
    successful = db.query(RecoveryAttempt).filter(
        RecoveryAttempt.status == "success"
    ).count()
    total_recovered = db.query(
        func.sum(RecoveryAttempt.recovered_amount)
    ).filter(RecoveryAttempt.status == "success").scalar() or 0

    return {
        "total_analyses": total,
        "successful_recoveries": successful,
        "success_rate": round((successful / total * 100) if total > 0 else 0, 1),
        "total_recovered_amount": round(total_recovered, 2),
    }
