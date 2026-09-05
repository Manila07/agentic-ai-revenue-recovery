"""Wipe and reseed 50 realistic failed payments for demo."""
import random
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal, Base
from app.models.payment import Payment
from app.models.recovery import RecoveryAttempt

PAYMENT_METHODS = ["upi", "netbanking", "credit_card", "debit_card", "wallet"]
FAILURE_REASONS = [
    ("NETWORK_TIMEOUT", "Network timeout"),
    ("INSUFFICIENT_FUNDS", "Insufficient funds"),
    ("CARD_DECLINED", "Card declined"),
    ("3D_AUTH_FAILED", "3D authentication failed"),
    ("RATE_LIMITED", "Rate limited"),
    ("FRAUD_SUSPECTED", "Fraud suspected"),
    ("INTERNAL_ERROR", "Internal error"),
    ("EXPIRED_CARD", "Card expired"),
]


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for i in range(50):
            code, reason = random.choice(FAILURE_REASONS)
            amount = round(random.uniform(200, 85000), 2)
            success_rate = round(random.uniform(0.1, 0.95), 2)
            db.add(Payment(
                id=f"PAY_{random.randint(100000, 999999)}",
                merchant_id="MERCHANT_001",
                customer_id=f"CUST_{random.randint(100, 999)}",
                amount=amount,
                currency="INR",
                status="failed",
                failure_reason=reason,
                failure_code=code,
                payment_method=random.choice(PAYMENT_METHODS),
                retry_count=random.randint(0, 3),
                customer_total_payments=random.randint(1, 20),
                customer_success_rate=success_rate,
                customer_previous_retries=random.randint(0, 5),
            ))
        db.commit()
        print("✅ Seeded 50 failed payments.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
