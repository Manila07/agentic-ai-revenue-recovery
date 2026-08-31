from app.core.config import settings  # type: ignore[import-not-found]
from app.core.constants import RecoveryAction  # type: ignore[import-not-found]

class ApprovalRuleGuardrail:
    def requires_approval(self, payment, action: str) -> bool:
        if payment.amount > settings.HUMAN_APPROVAL_THRESHOLD:
            return True
        if action == RecoveryAction.ESCALATE:
            return True
        if action == RecoveryAction.RETRY and payment.amount > settings.MAX_AUTO_APPROVAL_AMOUNT:
            return True
        return False