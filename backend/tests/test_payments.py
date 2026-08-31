import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_payments():
    response = client.get("/api/v1/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_simulate_failure():
    response = client.post("/api/v1/payments/simulate-failure", json={"amount": 1000})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FAILED"
    assert data["amount"] == 1000