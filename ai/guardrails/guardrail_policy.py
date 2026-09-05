import json
from typing import Dict, Any, Tuple
from pathlib import Path

class GuardrailPolicy:
    def __init__(self, policy_file: str = None):
        if policy_file is None:
            # Use the path relative to THIS file (not CWD)
            policy_file = Path(__file__).parent / "policy.json"
        with open(policy_file, "r") as f:
            self.policy = json.load(f)

    def validate(self, action: str, context: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Returns (is_allowed, decision_type, reason)
        decision_type: "ALLOW", "NEEDS_APPROVAL", "BLOCK"
        """
        amount = context.get("amount", 0)
        risk_score = context.get("risk_score", 0)
        retries = context.get("retry_count", 0)
        category = context.get("failure_category", "UNKNOWN")

        # Block non-retryable
        if category in self.policy["non_retryable_failures"]:
            return False, "BLOCK", f"Failure category '{category}' is non-retryable."

        # Block high risk
        if risk_score > self.policy["max_risk_score"]:
            return False, "BLOCK", f"Risk score {risk_score} exceeds max allowed."

        # Need approval for high amount
        if amount > self.policy["auto_approval_limit"]:
            return False, "NEEDS_APPROVAL", f"Amount ₹{amount} exceeds auto approval limit."

        # Block if retries exhausted
        if retries >= self.policy["max_retries"]:
            return False, "BLOCK", f"Max retries ({self.policy['max_retries']}) reached."

        # If all pass
        return True, "ALLOW", "All checks passed."

    def get_policy_summary(self) -> Dict:
        return self.policy