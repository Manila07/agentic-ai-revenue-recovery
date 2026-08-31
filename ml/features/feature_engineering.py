import numpy as np
from typing import Dict

def extract_features(payment_data: Dict) -> np.ndarray:
    features = {
        "amount": normalize_amount(payment_data.get("amount", 0)),
        "failure_category": category_to_index(payment_data.get("failure_category", "UNKNOWN")),
        "customer_success_rate": payment_data.get("customer_success_rate", 0.8),
        "time_since_failure": min(payment_data.get("hours_since_failure", 1) / 24, 1.0),
        "retry_count": min(payment_data.get("retry_count", 0) / 3, 1.0),
        "is_high_value": 1.0 if payment_data.get("amount", 0) > 5000 else 0.0,
        "is_premium_customer": 1.0 if payment_data.get("segment") == "premium" else 0.0,
    }
    return np.array(list(features.values()))

def normalize_amount(amount: float) -> float:
    return min(amount / 10000, 1.0)

def category_to_index(category: str) -> float:
    categories = {
        "INSUFFICIENT_FUNDS": 0,
        "CARD_EXPIRED": 1,
        "CARD_DECLINED": 2,
        "NETWORK_ERROR": 3,
        "BANK_UNAVAILABLE": 4,
        "LIMIT_EXCEEDED": 5,
        "INVALID_CVV": 6,
        "DUPLICATE": 7,
        "UNKNOWN": 8,
    }
    return categories.get(category, 8) / 8.0