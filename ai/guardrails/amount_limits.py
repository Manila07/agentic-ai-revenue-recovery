from typing import Optional, Tuple

try:
    from app.core.config import settings  # type: ignore
except ImportError:
    try:
        from core.config import settings  # type: ignore
    except ImportError:
        class _Settings:
            MAX_AUTO_APPROVAL_AMOUNT = float("inf")

        settings = _Settings()


class AmountLimitGuardrail:
    def __init__(self, max_amount: Optional[float] = None):
        self.max_amount: float = max_amount if max_amount is not None else settings.MAX_AUTO_APPROVAL_AMOUNT

    def check(self, amount: float) -> Tuple[bool, str]:
        if amount > self.max_amount:
            return False, f"Amount {amount} exceeds auto-approval limit {self.max_amount}"
        return True, "Amount within limit"