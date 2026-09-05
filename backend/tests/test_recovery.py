from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from backend.main import app

client = TestClient(app)


def test_analyze_payment():
    resp = client.post("/api/payments/simulate-failure", json={"amount": 500})
    assert resp.status_code == 200
    payment_id = resp.json()["id"]

    response = client.post(f"/api/recovery/{payment_id}/analyze")
    assert response.status_code == 200


def test_execute_recovery():
    resp = client.post("/api/payments/simulate-failure", json={"amount": 200})
    assert resp.status_code == 200
    payment_id = resp.json()["id"]

    response = client.post(f"/api/recovery/{payment_id}/execute?human_approved=false")
    assert response.status_code == 200
