from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(50), primary_key=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    segment = Column(String(50), default="standard")
    created_at = Column(DateTime, server_default=func.now())
    total_payments = Column(Integer, default=0)
    successful_payments = Column(Integer, default=0)
    failed_payments = Column(Integer, default=0)