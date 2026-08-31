from fastapi import APIRouter
from app.api.routes import payments, recovery, agent, analytics, webhooks, health, ws  # add ws


from app.api.routes import payments, recovery, agent, analytics, webhooks, health
api_router.include_router(ws.router, tags=["WebSocket"])
api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(recovery.router, prefix="/recovery", tags=["Recovery"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(webhooks.router, tags=["Webhooks"])
@router.post("/analyze/{payment_id}", response_model=RecoveryAnalysisOut)
async def analyze_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return await RecoveryService.analyze_payment(db, payment)

@router.post("/execute/{payment_id}", response_model=RecoveryExecuteOut)
async def execute_recovery(payment_id: str, data: RecoveryExecuteIn, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return await RecoveryService.execute_recovery(db, payment, data.action, data.approved_by)

@router.post("/approve/{payment_id}", response_model=RecoveryExecuteOut)
async def approve_recovery(payment_id: str, data: RecoveryApproveIn, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return await RecoveryService.approve_recovery(db, payment, data.approved_by)