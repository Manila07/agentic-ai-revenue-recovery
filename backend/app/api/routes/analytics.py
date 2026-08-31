from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.analytics import AnalyticsOverviewOut, RecoveryAnalyticsOut

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverviewOut)
async def get_overview(db: Session = Depends(get_db)):
    from app.services.analytics_service import AnalyticsService
    return AnalyticsService.get_overview(db)

@router.get("/recovery", response_model=RecoveryAnalyticsOut)
async def get_recovery_analytics(db: Session = Depends(get_db)):
    from app.services.analytics_service import AnalyticsService
    return AnalyticsService.get_recovery_analytics(db)