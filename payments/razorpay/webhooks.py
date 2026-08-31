from fastapi import Request, HTTPException
import hmac
import hashlib
import importlib


def _load_settings():
    for module_name in ("payments.core.config", "app.core.config"):
        try:
            return importlib.import_module(module_name).settings
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError("Could not import settings module")


settings = _load_settings()


async def verify_webhook_signature(request: Request, body: bytes):
    signature = request.headers.get("X-Razorpay-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    expected = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=400, detail="Invalid signature")