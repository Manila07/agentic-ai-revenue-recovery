from typing import Tuple

class ActionValidator:
    VALID_ACTIONS = {"RETRY", "NOTIFY", "WAIT", "ESCALATE", "STOP"}

    def validate(self, action: str, payment) -> Tuple[bool, str]:
        if action not in self.VALID_ACTIONS:
            return False, f"Invalid action: {action}"

        non_retryable = {"CARD_EXPIRED", "INVALID_CVV", "DUPLICATE"}
        if action in {"RETRY", "NOTIFY"} and payment.failure_category in non_retryable:
            return False, f"Cannot {action} for non-retryable failure: {payment.failure_category}"

        return True, "Valid"