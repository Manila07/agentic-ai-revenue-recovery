import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_notification(customer_id: str, message: str) -> dict:
        logger.info(f"Simulating notification to {customer_id}: {message}")
        return {"success": True, "message": f"Notification sent to {customer_id}: {message[:50]}..."}

    @staticmethod
    def send_email(customer_id: str, subject: str, body: str) -> dict:
        logger.info(f"Simulating email to {customer_id}: {subject}")
        return {"success": True, "message": f"Email sent: {subject}"}

    @staticmethod
    def send_sms(customer_id: str, message: str) -> dict:
        logger.info(f"Simulating SMS to {customer_id}: {message[:30]}...")
        return {"success": True, "message": f"SMS sent to {customer_id}"}