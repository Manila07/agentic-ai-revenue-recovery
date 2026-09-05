import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ai.agents.recovery_agent import RecoveryAgent


def test_recovery_agent_high_probability():
    agent = RecoveryAgent()
    result = agent.analyze({
        "payment_id": "PAY_TEST_HIGH",
        "failure_category": "NETWORK_ERROR",
        "amount": 5000,
        "customer_id": "CUST_TEST",
        "failure_reason": "Temporary network timeout",
    })
    assert result is not None
    assert isinstance(result, dict)


def test_recovery_agent_low_probability():
    agent = RecoveryAgent()
    result = agent.analyze({
        "payment_id": "PAY_TEST_LOW",
        "failure_category": "PERMANENT_FAILURE",
        "amount": 500,
        "customer_id": "CUST_TEST",
        "failure_reason": "Card permanently expired",
    })
    assert result is not None
    assert isinstance(result, dict)
