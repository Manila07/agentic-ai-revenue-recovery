import random
import uuid
from datetime import datetime
from typing import Dict, Optional

class PaymentSimulator:
    def __init__(self):
        self.failure_reasons = [
            "insufficient_funds",
            "card_expired",
            "card_declined",
            "network_error",
            "bank_unavailable",
            "limit_exceeded",
            "invalid_cvv",
            "duplicate_transaction",
            "processing_error",
        ]
        self.failure_categories = {
            "insufficient_funds": "INSUFFICIENT_FUNDS",
            "card_expired": "CARD_EXPIRED",
            "card_declined": "CARD_DECLINED",
            "network_error": "NETWORK_ERROR",
            "bank_unavailable": "BANK_UNAVAILABLE",
            "limit_exceeded": "LIMIT_EXCEEDED",
            "invalid_cvv": "INVALID_CVV",
            "duplicate_transaction": "DUPLICATE",
            "processing_error": "PROCESSING_ERROR",
        }

    def generate_failed_transaction(self, customer_id: Optional[str] = None, amount: Optional[float] = None, failure_reason: Optional[str] = None) -> Dict:
        if not customer_id:
            customer_id = f"cust_{uuid.uuid4().hex[:8]}"
        if not amount:
            amount = round(random.uniform(100, 10000), 2)
        if not failure_reason:
            failure_reason = random.choice(self.failure_reasons)
        return {
            "id": f"pay_{uuid.uuid4().hex[:12]}",
            "customer_id": customer_id,
            "amount": amount,
            "currency": "INR",
            "method": random.choice(["card", "upi", "netbanking"]),
            "status": "FAILED",
            "failure_reason": failure_reason,
            "failure_category": self.failure_categories.get(failure_reason, "UNKNOWN"),
            "created_at": datetime.now().isoformat(),
        }

    def generate_successful_transaction(self, customer_id: Optional[str] = None, amount: Optional[float] = None) -> Dict:
        if not customer_id:
            customer_id = f"cust_{uuid.uuid4().hex[:8]}"
        if not amount:
            amount = round(random.uniform(100, 10000), 2)
        return {
            "id": f"pay_{uuid.uuid4().hex[:12]}",
            "customer_id": customer_id,
            "amount": amount,
            "currency": "INR",
            "method": random.choice(["card", "upi", "netbanking"]),
            "status": "SUCCESS",
            "failure_reason": None,
            "failure_category": None,
            "created_at": datetime.now().isoformat(),
        }