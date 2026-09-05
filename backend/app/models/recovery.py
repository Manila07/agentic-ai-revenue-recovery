from sqlalchemy import Column, String, Float, Boolean, Text, DateTime
from app.database import Base
from datetime import datetime


class RecoveryAttempt(Base):
    __tablename__ = "recovery_attempts"

    id = Column(String, primary_key=True)
    payment_id = Column(String, nullable=False, index=True)
    strategy = Column(String, nullable=False)
    status = Column(String, nullable=False)  # success / failed / pending
    recovered_amount = Column(Float, default=0)
    explanation = Column(Text, default="")
    recovery_probability = Column(Float, default=0)
    risk_score = Column(Float, default=0)
    human_approved = Column(Boolean, default=False)
    simulated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
