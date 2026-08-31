import httpx
import hashlib
import hmac
import uuid
from typing import Dict, Optional
from fastapi import HTTPException
from app.core.config import settings

class RazorpayClient:
    """
    Official Razorpay API Client for Test Mode.
    Handles Order Creation, Payment Fetch, and Refund Initiation.
    """
    def __init__(self):
        self.base_url = "https://api.razorpay.com/v1"
        self.auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)

    async def create_order(self, amount: float, currency: str = "INR", receipt: Optional[str] = None) -> Dict:
        """Create a Razorpay Order. Amount should be in the smallest unit (e.g., paise) [citation:1]."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/orders",
                auth=self.auth,
                json={
                    "amount": int(amount * 100),  # Convert to paise
                    "currency": currency,
                    "receipt": receipt or f"receipt_{uuid.uuid4().hex[:8]}",
                },
            )
            response.raise_for_status()
            return response.json()

    async def fetch_payment(self, payment_id: str) -> Dict:
        """Fetch details of a specific payment."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/payments/{payment_id}",
                auth=self.auth,
            )
            response.raise_for_status()
            return response.json()

    async def create_refund(self, payment_id: str, amount: float, idempotency_key: str) -> Dict:
        """
        Initiate a refund.
        Uses Idempotency Key header (X-Refund-Idempotency) to ensure safe retries [citation:3].
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/payments/{payment_id}/refund",
                auth=self.auth,
                headers={
                    "Content-Type": "application/json",
                    "X-Refund-Idempotency": idempotency_key,
                },
                json={
                    "amount": int(amount * 100),
                    "speed": "optimum",
                    "receipt": f"refund_{uuid.uuid4().hex[:8]}",
                },
            )
            response.raise_for_status()
            return response.json()

    def verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        """
        Verify Razorpay Webhook Signature using HMAC SHA256.
        This is CRITICAL for security [citation:14].
        """
        expected = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)