from typing import Dict, Any

FAILURE_MAP = {
    "insufficient_funds": "INSUFFICIENT_FUNDS",
    "card_expired": "CARD_EXPIRED",
    "card_declined": "CARD_DECLINED",
    "network_error": "NETWORK_ERROR",
    "bank_unavailable": "BANK_UNAVAILABLE",
    "limit_exceeded": "LIMIT_EXCEEDED",
    "invalid_cvv": "INVALID_CVV",
    "duplicate_transaction": "DUPLICATE",
    "processing_error": "PROCESSING_ERROR",
}

class FailureAnalysisAgent:
    def analyze(self, failure_reason: str) -> Dict[str, Any]:
        reason = (failure_reason or "").lower().strip()
        category = FAILURE_MAP.get(reason, "UNKNOWN")
        retryable_categories = {"INSUFFICIENT_FUNDS", "NETWORK_ERROR", "BANK_UNAVAILABLE", "LIMIT_EXCEEDED", "PROCESSING_ERROR"}

        return {
            "failure_reason": failure_reason,
            "category": category,
            "retryable": category in retryable_categories,
            "recommended_cooldown": 3600 if category in {"NETWORK_ERROR", "BANK_UNAVAILABLE"} else 0,
        }