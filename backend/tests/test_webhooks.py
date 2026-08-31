import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_webhook_failed_payment():
    payload = {
        "event": "payment.failed",
        "payload": {
            "payment": {
                "id": "pay_test123",
                "customer_id": "cust_001",
                "amount": 5000,
                "failure_reason": "insufficient_funds",
                "failure_category": "INSUFFICIENT_FUNDS",
            }
        }
    }
    response = client.post("/api/v1/webhooks/payment", json=payload)
    assert response.status_code == 200
    assert response.json()["received"] == True