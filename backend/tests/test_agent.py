import pytest
from ai.agents.recovery_agent import RecoveryAgent
from ai.guardrails.action_validator import ActionValidator

def test_recovery_agent_high_probability():
    agent = RecoveryAgent()
    payment = type("Payment", (), {"failure_category": "INSUFFICIENT_FUNDS"})()
    result = agent.analyze(payment, 0.85)
    assert result["decision"] == "RETRY"

def test_recovery_agent_low_probability():
    agent = RecoveryAgent()
    payment = type("Payment", (), {"failure_category": "INSUFFICIENT_FUNDS"})()
    result = agent.analyze(payment, 0.2)
    assert result["decision"] == "STOP"

def test_action_validator_non_retryable():
    validator = ActionValidator()
    payment = type("Payment", (), {"failure_category": "CARD_EXPIRED"})()
    valid, error = validator.validate("RETRY", payment)
    assert not valid