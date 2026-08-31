from fastapi import APIRouter, Request, HTTPException, Header
from payments.razorpay.client import RazorpayClient
from app.services.real_time_service import manager
import json

router = APIRouter()

@router.post("/webhooks/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
):
    """
    Handle REAL Razorpay Webhooks (Test Mode).
    Verify signature, process event, broadcast to frontend.
    """
    body = await request.body()
    razorpay = RazorpayClient()
    
    # 1. Security First: Verify Signature [citation:14]
    if not razorpay.verify_webhook_signature(body, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid Signature")
    
    payload = json.loads(body)
    event_type = payload.get("event")
    
    # 2. Process Real Event
    if event_type == "payment.failed":
        data = payload["payload"]["payment"]["entity"]
        # Convert to our model and trigger recovery workflow
        # ... (similar to your existing webhook logic but with REAL data)
        
        # 3. Real-Time Broadcast to Dashboard
        await manager.broadcast(json.dumps({
            "type": "PAYMENT_FAILED",
            "payment_id": data["id"],
            "amount": data["amount"] / 100,
        }))
    
    elif event_type == "payment.captured":
        await manager.broadcast(json.dumps({
            "type": "PAYMENT_RECOVERED",
            "payment_id": data["id"],
        }))

    return {"received": True}