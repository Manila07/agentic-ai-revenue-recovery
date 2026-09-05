from fastapi import APIRouter
from app.api.routes import health, payments, recovery, agent, analytics, webhooks, ws

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(recovery.router, prefix="/recovery", tags=["Recovery"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(ws.router, tags=["WebSocket"])
