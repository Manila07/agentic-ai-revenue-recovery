from typing import Dict

class PaymentFailureWorkflow:
    def process(self, payment_data: Dict) -> Dict:
        return {
            "payment_id": payment_data.get("id"),
            "status": "FAILED",
            "failure_reason": payment_data.get("failure_reason", "UNKNOWN"),
            "needs_recovery": True,
        }