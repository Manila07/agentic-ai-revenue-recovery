"""
Advanced Recovery Agent with Tool-Calling Loop.
Evaluates multiple factors (amount, risk, history, failure type, retry count)
and selects a strategy using a deterministic reasoning engine (rule-based planning).
"""
from typing import Dict, Any, List
from dataclasses import dataclass, field
import json

# --- Tool Definitions (Abstracted as functions) ---
class Tools:
    @staticmethod
    def get_payment(payment_id: str) -> Dict:
        return {"payment_id": payment_id, "amount": 10000, "failure_reason": "insufficient_funds"}

    @staticmethod
    def get_customer_history(customer_id: str) -> Dict:
        return {"customer_id": customer_id, "success_rate": 0.75, "total_failures": 3}

    @staticmethod
    def calculate_risk_score(amount: float, customer_success_rate: float) -> float:
        # Risk score 0-1 (higher means more risky)
        amount_risk = min(amount / 100000, 1.0)
        history_risk = (1 - customer_success_rate) * 0.5
        return min(amount_risk * 0.6 + history_risk, 1.0)

    @staticmethod
    def predict_recovery_probability(payment: Dict) -> float:
        # Simulated ML prediction (replace with actual ML model call later)
        failure_categories = {"insufficient_funds": 0.8, "network_error": 0.6, "card_declined": 0.3, "expired_card": 0.1}
        return failure_categories.get(payment.get("failure_reason", "unknown"), 0.4)

    @staticmethod
    def request_human_approval(payment_id: str, reason: str) -> Dict:
        return {"status": "PENDING", "payment_id": payment_id, "reason": reason}

    @staticmethod
    def execute_retry(payment_id: str) -> Dict:
        return {"success": True, "message": "Retry executed successfully"}

    @staticmethod
    def send_notification(customer_id: str, message: str) -> Dict:
        return {"success": True, "message": f"Notification sent to {customer_id}"}

    @staticmethod
    def stop_recovery(payment_id: str) -> Dict:
        return {"success": True, "message": "Recovery stopped"}

    @staticmethod
    def wait_and_retry(payment_id: str, delay_minutes: int) -> Dict:
        return {"success": True, "message": f"Retry scheduled in {delay_minutes} minutes"}

# --- Agent ---
class RecoveryAgent:
    def __init__(self):
        self.tools = Tools()
        self.max_retries = 3
        self.cooldown_minutes = 60

    def analyze(self, payment: Dict) -> Dict[str, Any]:
        """
        Main agent loop:
        Observe -> Analyze -> Predict -> Plan -> Validate -> Act
        """
        # 1. Observe: Gather data
        payment_id = payment["payment_id"]
        customer = self.tools.get_customer_history(payment.get("customer_id", "unknown"))
        risk_score = self.tools.calculate_risk_score(payment.get("amount", 0), customer["success_rate"])
        recovery_prob = self.tools.predict_recovery_probability(payment)

        # 2. Analyze: Determine failure category retryability
        non_retryable = {"expired_card", "invalid_cvv", "duplicate"}
        is_retryable = payment.get("failure_reason", "unknown") not in non_retryable

        # 3. Plan: Select strategy based on multiple factors
        reasoning_trace = []
        if not is_retryable:
            decision = "STOP"
            reasoning_trace.append("Failure category is non-retryable.")
        elif risk_score > 0.85:
            decision = "BLOCK"
            reasoning_trace.append("Risk score too high. Blocking automatic recovery.")
        elif payment.get("amount", 0) > 50000:
            decision = "ESCALATE"
            reasoning_trace.append("High transaction value requires human approval.")
        elif recovery_prob > 0.75:
            decision = "RETRY"
            reasoning_trace.append(f"High recovery probability ({recovery_prob:.2f}) and low risk ({risk_score:.2f}).")
        elif recovery_prob > 0.5:
            decision = "WAIT"
            reasoning_trace.append(f"Moderate recovery probability ({recovery_prob:.2f}). Waiting for cooldown.")
        elif recovery_prob > 0.3:
            decision = "NOTIFY"
            reasoning_trace.append(f"Low probability ({recovery_prob:.2f}). Notifying customer to take action.")
        else:
            decision = "STOP"
            reasoning_trace.append("Recovery probability too low to justify action.")

        # 4. Act: Execute tool based on decision (simulated here, but wired to actual workflow in service)
        tool_calls = []
        if decision == "RETRY":
            tool_calls.append({"tool": "execute_retry", "args": {"payment_id": payment_id}})
        elif decision == "NOTIFY":
            tool_calls.append({"tool": "send_notification", "args": {"customer_id": payment.get("customer_id"), "message": "Please update payment method"}})
        elif decision == "WAIT":
            tool_calls.append({"tool": "wait_and_retry", "args": {"payment_id": payment_id, "delay_minutes": self.cooldown_minutes}})
        elif decision == "ESCALATE":
            tool_calls.append({"tool": "request_human_approval", "args": {"payment_id": payment_id, "reason": "Amount exceeds threshold"}})
        elif decision == "STOP":
            tool_calls.append({"tool": "stop_recovery", "args": {"payment_id": payment_id}})

        return {
            "payment_id": payment_id,
            "decision": decision,
            "confidence": recovery_prob,
            "risk_score": risk_score,
            "reasoning_trace": reasoning_trace,
            "tool_calls": tool_calls,
        }