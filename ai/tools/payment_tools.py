from typing import Dict, Any, Optional

class PaymentTools:
    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        return {"payment_id": payment_id, "status": "FAILED"}

    def retry_payment(self, payment_id: str, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        return {"success": True, "message": "Retry executed"}

    def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        return {"payment_id": payment_id, "verified": True}