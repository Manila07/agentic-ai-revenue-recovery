class SafetyPolicy:
    def __init__(self):
        self.policy = {
            "max_retries_per_payment": 3,
            "cooldown_seconds": 3600,
            "max_auto_approval_amount": 5000,
            "require_human_approval_for_escalation": True,
            "block_non_retryable_failures": True,
        }

    def check(self, rule_name: str) -> bool:
        return self.policy.get(rule_name, True)

    def get_all_policies(self) -> dict:
        return self.policy