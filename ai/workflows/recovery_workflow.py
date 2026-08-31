from typing import Dict, Any
from ai.guardrails.action_validator import ActionValidator
from app.services.notification_service import NotificationService

class RecoveryWorkflow:
    def __init__(self):
        self.validator = ActionValidator()

    def execute(self, db, payment, action: str) -> Dict[str, Any]:
        valid, error = self.validator.validate(action, payment)
        if not valid:
            return {"success": False, "message": f"Invalid: {error}"}

        if action == "RETRY":
            return self._execute_retry(db, payment)
        elif action == "NOTIFY":
            return self._execute_notify(db, payment)
        elif action == "WAIT":
            return self._execute_wait(db, payment)
        elif action == "ESCALATE":
            return self._execute_escalate(db, payment)
        elif action == "STOP":
            return self._execute_stop(db, payment)
        else:
            return {"success": False, "message": f"Unknown action: {action}"}

    def _execute_retry(self, db, payment) -> Dict[str, Any]:
        success = payment.recovery_probability > 0.5
        return {
            "success": success,
            "message": "Payment retry successful!" if success else "Payment retry failed again.",
        }

    def _execute_notify(self, db, payment) -> Dict[str, Any]:
        result = NotificationService.send_notification(
            payment.customer_id,
            "Your payment needs attention. Please update payment method.",
        )
        return {"success": True, "message": result["message"]}

    def _execute_wait(self, db, payment) -> Dict[str, Any]:
        return {"success": True, "message": "Scheduled retry in cooldown period."}

    def _execute_escalate(self, db, payment) -> Dict[str, Any]:
        return {"success": True, "message": "Escalated to manual review team."}

    def _execute_stop(self, db, payment) -> Dict[str, Any]:
        return {"success": True, "message": "Recovery stopped for this payment."}