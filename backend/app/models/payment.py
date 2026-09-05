from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True)
    merchant_id = Column(String, index=True)
    customer_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String, default="failed")
    failure_reason = Column(String)
    failure_code = Column(String)
    payment_method = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    retry_count = Column(Integer, default=0)

    # Customer history
    customer_total_payments = Column(Integer, default=0)
    customer_successful_payments = Column(Integer, default=0)
    customer_failed_payments = Column(Integer, default=0)
    customer_success_rate = Column(Float, default=0.0)
    customer_previous_retries = Column(Integer, default=0)
