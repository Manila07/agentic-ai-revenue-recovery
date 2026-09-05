from fastapi import APIRouter

router = APIRouter()

@router.post("/payment")
def payment_webhook():
    return {"received": True}

@router.get("/events")
def webhook_events():
    return {"events": []}
