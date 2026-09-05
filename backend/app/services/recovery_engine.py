"""
Recovery Engine — Core AI Brain
Implements: Observe → Reason → Decide → Act → Evaluate
"""
import random
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.recovery import RecoveryAttempt


STRATEGIES = {
    "retry_payment": {
        "name": "Retry Payment",
        "description": "Retry payment using the same method after a short delay.",
        "risk_level": "low",
        "requires_human_approval": False,
        "success_rate": 0.65,
    },
    "retry_different_route": {
        "name": "Retry via Different Route",
        "description": "Attempt payment through an alternative gateway.",
        "risk_level": "low",
        "requires_human_approval": False,
        "success_rate": 0.55,
    },
    "send_reminder": {
        "name": "Send Payment Reminder",
        "description": "Send reminder to customer to complete payment.",
        "risk_level": "low",
        "requires_human_approval": False,
        "success_rate": 0.45,
    },
    "schedule_retry": {
        "name": "Schedule Retry",
        "description": "Schedule retry for optimal time window.",
        "risk_level": "low",
        "requires_human_approval": False,
        "success_rate": 0.50,
    },
    "generate_payment_link": {
        "name": "Generate Payment Link",
        "description": "Generate fresh payment link for the customer.",
        "risk_level": "medium",
        "requires_human_approval": False,
        "success_rate": 0.55,
    },
    "send_email": {
        "name": "Send Email Notification",
        "description": "Send detailed email explaining the failure.",
        "risk_level": "medium",
        "requires_human_approval": False,
        "success_rate": 0.40,
    },
    "escalate_human": {
        "name": "Escalate to Human Support",
        "description": "Route to human agent for manual follow-up.",
        "risk_level": "high",
        "requires_human_approval": True,
        "success_rate": 0.70,
    },
    "no_action": {
        "name": "No Action",
        "description": "Recovery probability too low. No automated action.",
        "risk_level": "none",
        "requires_human_approval": False,
        "success_rate": 0.0,
    },
}

FAILURE_CATEGORIES = {
    "network": {
        "codes": ["NETWORK_TIMEOUT", "CONNECTION_FAILED", "GATEWAY_TIMEOUT"],
        "base_probability": 0.75,
        "best_strategy": "retry_payment",
    },
    "insufficient_funds": {
        "codes": ["INSUFFICIENT_FUNDS"],
        "base_probability": 0.40,
        "best_strategy": "send_reminder",
    },
    "card_declined": {
        "codes": ["CARD_DECLINED", "EXPIRED_CARD", "INVALID_CARD"],
        "base_probability": 0.30,
        "best_strategy": "generate_payment_link",
    },
    "authentication": {
        "codes": ["3D_AUTH_FAILED", "OTP_FAILED", "AUTHENTICATION_REQUIRED"],
        "base_probability": 0.60,
        "best_strategy": "retry_different_route",
    },
    "rate_limit": {
        "codes": ["RATE_LIMITED", "TOO_MANY_ATTEMPTS"],
        "base_probability": 0.55,
        "best_strategy": "schedule_retry",
    },
    "fraud_suspected": {
        "codes": ["FRAUD_SUSPECTED", "RISK_THRESHOLD_EXCEEDED"],
        "base_probability": 0.10,
        "best_strategy": "escalate_human",
    },
    "technical": {
        "codes": ["INTERNAL_ERROR", "SERVICE_UNAVAILABLE", "UNKNOWN_ERROR"],
        "base_probability": 0.65,
        "best_strategy": "retry_different_route",
    },
}


def classify_failure(failure_code: str) -> dict:
    """Classify failure into category."""
    for category, info in FAILURE_CATEGORIES.items():
        if failure_code in info["codes"]:
            return {"category": category, **info}
    return {"category": "unknown", "codes": [], "base_probability": 0.35, "best_strategy": "send_reminder"}


def predict_recovery_probability(payment, classification: dict) -> float:
    """Predict recovery probability based on context."""
    base = classification["base_probability"]
    
    # Adjust based on retry count
    retry_penalty = min(payment.retry_count * 0.08, 0.3)
    base -= retry_penalty
    
    # Adjust based on customer history
    if payment.customer_success_rate:
        history_bonus = (payment.customer_success_rate - 0.5) * 0.2
        base += history_bonus
    
    # Amount penalty for very large payments
    if payment.amount > 50000:
        base -= 0.1
    elif payment.amount < 1000:
        base += 0.1
    
    return max(0.05, min(0.95, base))


def calculate_risk_score(payment) -> float:
    """Calculate risk score (0=low risk, 1=high risk)."""
    risk = 0.2  # base
    if payment.amount > 50000:
        risk += 0.3
    if payment.retry_count > 3:
        risk += 0.2
    if payment.failure_code in ["FRAUD_SUSPECTED", "RISK_THRESHOLD_EXCEEDED"]:
        risk += 0.4
    return min(0.95, risk)


def select_strategy(probability: float, risk_score: float, classification: dict) -> dict:
    """Select the best recovery strategy."""
    if probability < 0.15:
        return STRATEGIES["no_action"]
    if risk_score > 0.7:
        return STRATEGIES["escalate_human"]
    
    best_key = classification["best_strategy"]
    strategy = STRATEGIES[best_key].copy()
    strategy["key"] = best_key
    
    if risk_score > 0.5 and strategy["risk_level"] == "low":
        strategy["requires_human_approval"] = True
    
    return strategy


def analyze_payment(db: Session, payment_id: str) -> dict:
    """
    OBSERVE → REASON → DECIDE
    Analyze a failed payment and return AI decision.
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError(f"Payment {payment_id} not found")
    
    # OBSERVE
    classification = classify_failure(payment.failure_code or "UNKNOWN_ERROR")
    
    # REASON
    probability = predict_recovery_probability(payment, classification)
    risk_score = calculate_risk_score(payment)
    
    # DECIDE
    strategy = select_strategy(probability, risk_score, classification)
    
    explanation = (
        f"Payment {payment.id} failed due to {classification['category'].replace('_', ' ')}. "
        f"Customer has {payment.customer_total_payments or 0} prior payments with "
        f"{((payment.customer_success_rate or 0) * 100):.0f}% success rate. "
        f"Recovery probability: {probability*100:.1f}%. "
        f"Selected strategy: {strategy['name']} ({strategy['description']})"
    )
    
    return {
        "payment_id": payment.id,
        "recovery_probability": round(probability, 3),
        "risk_score": round(risk_score, 3),
        "failure_category": classification["category"],
        "selected_strategy": {
            "key": strategy.get("key", strategy["name"]),
            "name": strategy["name"],
            "description": strategy["description"],
            "risk_level": strategy["risk_level"],
            "requires_human_approval": strategy["requires_human_approval"],
        },
        "explanation": explanation,
    }


def execute_recovery(db: Session, payment_id: str, human_approved: bool = False) -> dict:
    """
    ACT → EVALUATE
    Execute the recovery action and record the result.
    """
    analysis = analyze_payment(db, payment_id)
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    strategy = analysis["selected_strategy"]
    
    # Guardrails
    if strategy["requires_human_approval"] and not human_approved:
        return {
            "success": False,
            "requires_human_approval": True,
            "payment_id": payment_id,
            "strategy": strategy["name"],
            "message": "This action requires human approval before execution.",
            "analysis": analysis,
        }
    
    # Simulate execution
    success_rate = STRATEGIES.get(strategy.get("key", ""), {}).get("success_rate", 0.5)
    simulated_success = random.random() < success_rate
    
    recovered_amount = payment.amount if simulated_success else 0
    status = "success" if simulated_success else "failed"
    
    # Record attempt
    attempt = RecoveryAttempt(
        id=f"REC_{uuid.uuid4().hex[:8].upper()}",
        payment_id=payment_id,
        strategy=strategy.get("key", strategy["name"]),
        status=status,
        recovered_amount=recovered_amount,
        explanation=analysis["explanation"],
        recovery_probability=analysis["recovery_probability"],
        risk_score=analysis["risk_score"],
        human_approved=human_approved,
        simulated=True,
    )
    db.add(attempt)
    
    # Update payment status
    if simulated_success:
        payment.status = "recovered"
    payment.retry_count = (payment.retry_count or 0) + 1
    
    db.commit()
    
    return {
        "success": simulated_success,
        "payment_id": payment_id,
        "strategy": strategy["name"],
        "recovered_amount": recovered_amount,
        "message": f"Recovery {'succeeded' if simulated_success else 'failed'} via {strategy['name']}.",
        "analysis": analysis,
    }
