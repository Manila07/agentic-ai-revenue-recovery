from typing import Dict, Any

class CustomerTools:
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return {"customer_id": customer_id, "segment": "standard", "risk_score": 0.3}

    def get_customer_history(self, customer_id: str) -> Dict[str, Any]:
        return {"customer_id": customer_id, "total_payments": 25, "successful": 22, "failed": 3, "success_rate": 0.88}