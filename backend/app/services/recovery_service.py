"""
Recovery Service
Provides high-level recovery operations, wrapping the core recovery engine.
"""
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.recovery import RecoveryAttempt
from app.services.recovery_engine import analyze_payment, execute_recovery
from app.services.event_bus import event_bus
from typing import Dict, Any
import asyncio


async def analyze_payment_service(db: Session, payment_id: str) -> Dict[str, Any]:
    """
    Analyze a payment and return the AI's decision.
    """
    return analyze_payment(db, payment_id)


async def execute_recovery_service(
    db: Session, payment_id: str, human_approved: bool = False
) -> Dict[str, Any]:
    """
    Execute a recovery action for a payment.
    """
    result = execute_recovery(db, payment_id, human_approved)
    
    # Broadcast event for WebSocket updates
    if result.get("success"):
        asyncio.get_event_loop().create_task(
            event_bus.broadcast(
                "recovery_executed",
                {
                    "payment_id": payment_id,
                    "strategy": result.get("strategy"),
                    "recovered_amount": result.get("recovered_amount", 0),
                },
            )
        )
    
    return result


def get_recovery_history(db: Session, payment_id: str):
    """
    Get all recovery attempts for a payment.
    """
    return (
        db.query(RecoveryAttempt)
        .filter(RecoveryAttempt.payment_id == payment_id)
        .order_by(RecoveryAttempt.created_at.desc())
        .all()
    )
