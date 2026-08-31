from typing import Dict

class CommunicationAgent:
    def generate_notification(self, payment, action: str) -> Dict:
        amount = payment.amount
        currency = payment.currency or "INR"
        messages = {
            "NOTIFY": f"We noticed your payment of {currency} {amount:,.2f} failed due to {payment.failure_reason}. Please update your payment method and retry.",
            "RETRY": f"We attempted to retry your payment of {currency} {amount:,.2f}.",
            "WAIT": f"We'll retry your payment of {currency} {amount:,.2f} shortly.",
        }
        return {
            "message": messages.get(action, "Your payment needs attention."),
            "channel": "email",
            "severity": "info" if action != "ESCALATE" else "warning",
        }