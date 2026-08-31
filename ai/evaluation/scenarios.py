SCENARIOS = [
    {
        "payment": {
            "amount": 1000,
            "failure_reason": "insufficient_funds",
            "failure_category": "INSUFFICIENT_FUNDS",
            "recovery_probability": 0.85,
        },
        "expected": "RETRY",
    },
    {
        "payment": {
            "amount": 500,
            "failure_reason": "card_expired",
            "failure_category": "CARD_EXPIRED",
            "recovery_probability": 0.1,
        },
        "expected": "STOP",
    },
    {
        "payment": {
            "amount": 2000,
            "failure_reason": "network_error",
            "failure_category": "NETWORK_ERROR",
            "recovery_probability": 0.6,
        },
        "expected": "NOTIFY",
    },
    {
        "payment": {
            "amount": 10000,
            "failure_reason": "bank_unavailable",
            "failure_category": "BANK_UNAVAILABLE",
            "recovery_probability": 0.75,
        },
        "expected": "RETRY",
    },
]