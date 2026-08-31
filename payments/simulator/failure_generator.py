import random
import uuid
from typing import Dict

class FailureGenerator:
    def __init__(self):
        self.scenarios = {
            "insufficient_funds": {"amount": random.uniform(100, 5000), "reason": "insufficient_funds", "category": "INSUFFICIENT_FUNDS"},
            "card_expired": {"amount": random.uniform(100, 5000), "reason": "card_expired", "category": "CARD_EXPIRED"},
            "network_error": {"amount": random.uniform(100, 5000), "reason": "network_error", "category": "NETWORK_ERROR"},
            "bank_unavailable": {"amount": random.uniform(100, 5000), "reason": "bank_unavailable", "category": "BANK_UNAVAILABLE"},
        }

    def generate(self, scenario: str) -> Dict:
        if scenario not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario}")
        data = self.scenarios[scenario]
        return {
            "id": f"pay_{uuid.uuid4().hex[:12]}",
            "customer_id": f"cust_{uuid.uuid4().hex[:8]}",
            "amount": data["amount"],
            "currency": "INR",
            "method": "card",
            "status": "FAILED",
            "failure_reason": data["reason"],
            "failure_category": data["category"],
        }