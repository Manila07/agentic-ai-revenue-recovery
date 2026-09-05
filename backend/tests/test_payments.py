from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200


def test_list_payments():
    response = client.get("/api/payments")
    assert response.status_code == 200


def test_simulate_failure():
    response = client.post("/api/payments/simulate-failure", json={"amount": 1000})
    assert response.status_code == 200
