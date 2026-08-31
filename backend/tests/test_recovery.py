import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_analyze_payment():
    # Create a simulated failure first
    resp = client.post("/api/v1/payments/simulate-failure", json={"amount": 500})
    payment_id = resp.json()["id"]
    response = client.post(f"/api/v1/recovery/analyze/{payment_id}")
    assert response.status_code == 200
    data = response.json()
    assert "recommended_action" in data
    assert data["recovery_probability"] >= 0.0

def test_execute_recovery():
    resp = client.post("/api/v1/payments/simulate-failure", json={"amount": 200})
    payment_id = resp.json()["id"]
    # Analyze first
    client.post(f"/api/v1/recovery/analyze/{payment_id}")
    response = client.post(f"/api/v1/recovery/execute/{payment_id}", json={"action": "STOP"})
    assert response.status_code == 200
    assert response.json()["success"] == True