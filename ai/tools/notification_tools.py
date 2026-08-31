from typing import Dict, Any

class NotificationTools:
    def send_notification(self, customer_id: str, message: str) -> Dict[str, Any]:
        return {"success": True, "message": f"Notification sent to {customer_id}"}

    def schedule_notification(self, customer_id: str, message: str, delay_seconds: int) -> Dict[str, Any]:
        return {"success": True, "message": f"Notification scheduled in {delay_seconds}s"}