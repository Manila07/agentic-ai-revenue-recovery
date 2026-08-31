class MockPaymentAPI:
    def get_payment(self, payment_id: str):
        return {"payment_id": payment_id, "status": "FAILED"}

    def retry_payment(self, payment_id: str):
        return {"success": True}