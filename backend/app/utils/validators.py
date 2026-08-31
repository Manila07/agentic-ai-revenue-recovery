def validate_positive_amount(amount: float):
    if amount <= 0:
        return False, "Amount must be positive"
    return True, None

def validate_payment_id(payment_id: str):
    if not payment_id or len(payment_id) < 5:
        return False, "Payment ID must be at least 5 characters"
    return True, None

def validate_action(action: str):
    allowed = {"RETRY", "NOTIFY", "WAIT", "ESCALATE", "STOP"}
    if action not in allowed:
        return False, f"Action must be one of {allowed}"
    return True, None