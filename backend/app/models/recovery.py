from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class RecoveryAttempt(Base):
    __tablename__ = "recovery_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String(50), ForeignKey("payments.id"), nullable=False)
    attempt_number = Column(Integer, default=1)
    action = Column(String(50), nullable=False)
    scheduled_at = Column(DateTime, server_default=func.now())
    executed_at = Column(DateTime)
    result = Column(String(50))
    status = Column(String(20), default="PENDING")