from typing import Optional, Tuple

try:
    from app.core.config import settings  # pyright: ignore[reportMissingImports]
except ImportError:
    class _FallbackSettings:
        MAX_RETRIES_PER_PAYMENT = 3

    settings = _FallbackSettings()


class RetryLimitGuardrail:
    def __init__(self, max_retries: Optional[int] = None):
        self.max_retries: int = (
            max_retries if max_retries is not None else settings.MAX_RETRIES_PER_PAYMENT
        )

    def check(self, current_retry_count: int) -> Tuple[bool, str]:
        if current_retry_count >= self.max_retries:
            return False, f"Maximum retries ({self.max_retries}) reached"
        return True, "Retry allowed"