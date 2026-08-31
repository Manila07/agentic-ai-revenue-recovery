"""
Recovery Agent - main agent for recovery decision.
"""
from typing import Dict, Any

class RecoveryAgent:
    def __init__(self):
        self.actions = ["RETRY", "NOTIFY", "WAIT", "ESCALATE", "STOP"]

    def analyze(self, payment, recovery_probability: float) -> Dict[str, Any]:
        failure_category = payment.failure_category or "UNKNOWN"
        non_retryable = {"CARD_EXPIRED", "INVALID_CVV", "DUPLICATE"}

        if failure_category in non_retryable:
            return {
                "decision": "STOP",
                "reasoning": f"Failure category '{failure_category}' is not retryable.",
                "confidence": 0.95,
            }

        if recovery_probability > 0.7:
            return {
                "decision": "RETRY",
                "reasoning": f"High recovery probability ({recovery_probability:.2f}). Attempting immediate retry.",
                "confidence": recovery_probability,
            }
        elif recovery_probability > 0.4:
            return {
                "decision": "NOTIFY",
                "reasoning": f"Moderate recovery probability ({recovery_probability:.2f}). Notify customer to resolve issue.",
                "confidence": recovery_probability,
            }
        else:
            return {
                "decision": "STOP",
                "reasoning": f"Low recovery probability ({recovery_probability:.2f}). Not worth retrying automatically.",
                "confidence": 1.0 - recovery_probability,
            }