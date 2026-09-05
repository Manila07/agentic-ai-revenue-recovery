"""
Realistic payment failure simulator for demo purposes.
Generates failed payments with believable patterns.
"""
import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.payment import Payment


FAILURE_SCENARIOS = [
    {
        "failure_reason": "insufficient_funds",
        "failure_code": "INSUFFICIENT_FUNDS",
        "recovery_potential": 0.72,
        "description": "Customer account has insufficient balance",
    },
    {
        "failure_reason": "network_timeout",
        "failure_code": "NETWORK_TIMEOUT",
        "recovery_potential": 0.91,
        "description": "Payment gateway connection timed out",
    },
    {
        "failure_reason": "card_expired",
        "failure_code": "CARD_EXPIRED",
        "recovery_potential": 0.35,
        "description": "Credit/debit card has expired",
    },
    {
        "failure_reason": "bank_declined",
        "failure_code": "BANK_DECLINED",
        "recovery_potential": 0.48,
        "description": "Issuing bank rejected the transaction",
    },
    {
        "failure_reason": "authentication_failed",
        "failure_code": "AUTH_FAILED",
        "recovery_potential": 0.67,
        "description": "3D Secure / OTP verification failed",
    },
    {
        "failure_reason": "rate_limited",
        "failure_code": "RATE_LIMITED",
        "recovery_potential": 0.88,
        "description": "Too many payment attempts in short window",
    },
    {
        "failure_reason": "fraud_suspected",
        "failure_code": "FRAUD_HOLD",
        "recovery_potential": 0.15,
        "description": "Transaction flagged by fraud detection",
    },
    {
        "failure_reason": "technical_error",
        "failure_code": "TECH_ERROR",
        "recovery_potential": 0.82,
        "description": "Internal payment processor error",
    },
]

PAYMENT_METHODS = [
    "upi", "credit_card", "debit_card", "net_banking",
    "wallet", "emi", "pay_later",
]

CURRENCIES = ["INR"]

AMOUNT_RANGES = [
    (99, 500),       # Small
    (500, 2000),     # Medium
    (2000, 10000),   # Large
    (10000, 50000),  # Enterprise
]

MERCHANTS = [
    "MERCHANT_001", "MERCHANT_002", "MERCHANT_003",
    "MERCHANT_004", "MERCHANT_005",
]


def generate_customer_profile():
    """Generate a realistic customer payment history."""
    total = random.randint(5, 200)
    success_rate = random.betavariate(2, 1)  # Skewed toward high success
    successful = int(total * success_rate)
    failed = total - successful
    return {
        "total_payments": total,
        "successful_payments": successful,
        "failed_payments": failed,
        "success_rate": round(success_rate, 3),
        "previous_retries": random.randint(0, min(failed, 5)),
    }


def generate_single_failed_payment() -> dict:
    """Generate one realistic failed payment."""
    scenario = random.choice(FAILURE_SCENARIOS)
    amount_range = random.choice(AMOUNT_RANGES)
    amount = round(random.uniform(*amount_range), 2)
    customer = generate_customer_profile()
    
    # Time in last 7 days, with more recent failures
    hours_ago = random.expovariate(1 / 48)  # Average ~2 days ago
    created_at = datetime.utcnow() - timedelta(hours=min(hours_ago, 168))
    
    # More successful history → higher actual recovery chance
    base_prob = scenario["recovery_potential"]
    history_boost = customer["success_rate"] * 0.15
    recovery_probability = min(base_prob + history_boost, 0.99)
    
    return {
        "id": f"PAY_{random.randint(10000, 99999)}",
        "merchant_id": random.choice(MERCHANTS),
        "customer_id": f"CUST_{random.randint(1000, 9999)}",
        "amount": amount,
        "currency": "INR",
        "status": "failed",
        "failure_reason": scenario["failure_reason"],
        "failure_code": scenario["failure_code"],
        "payment_method": random.choice(PAYMENT_METHODS),
        "created_at": created_at,
        "retry_count": random.randint(0, 3),
        "customer_total_payments": customer["total_payments"],
        "customer_successful_payments": customer["successful_payments"],
        "customer_failed_payments": customer["failed_payments"],
        "customer_success_rate": customer["success_rate"],
        "customer_previous_retries": customer["previous_retries"],
    }


def seed_payments(db: Session, count: int = 50) -> int:
    """Seed database with realistic failed payments."""
    existing = db.query(Payment).count()
    if existing >= count:
        return 0
    
    generated = []
    for _ in range(count - existing):
        data = generate_single_failed_payment()
        payment = Payment(**data)
        db.add(payment)
        generated.append(data)
    
    db.commit()
    return len(generated)


def generate_new_payment_stream() -> dict:
    """Generate a single new failed payment (for real-time simulation)."""
    return generate_single_failed_payment()
