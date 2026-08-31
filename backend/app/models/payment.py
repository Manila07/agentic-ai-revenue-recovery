from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    method = Column(String(50), default="card")
    status = Column(String(20), default="FAILED")
    failure_reason = Column(String(255))
    failure_category = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    recovered = Column(Boolean, default=False)
    recovered_amount = Column(Float, default=0.0)
    recovery_probability = Column(Float, default=0.0)