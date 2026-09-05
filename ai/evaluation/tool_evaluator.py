SCENARIOS = [
    {
        "id": "SC-01",
        "payment": {
            "payment_id": "pay_001", "customer_id": "cust_001", "amount": 500,
            "failure_reason": "insufficient_funds", "failure_category": "INSUFFICIENT_FUNDS",
            "retry_count": 0
        },
        "expected_decision": "RETRY"
    },
    {
        "id": "SC-02",
        "payment": {
            "payment_id": "pay_002", "customer_id": "cust_002", "amount": 250000,
            "failure_reason": "network_error", "failure_category": "NETWORK_ERROR",
            "retry_count": 0
        },
        "expected_decision": "ESCALATE"
    },
    {
        "id": "SC-03",
        "payment": {
            "payment_id": "pay_003", "customer_id": "cust_003", "amount": 1000,
            "failure_reason": "card_expired", "failure_category": "CARD_EXPIRED",
            "retry_count": 2
        },
        "expected_decision": "STOP"
    }
]