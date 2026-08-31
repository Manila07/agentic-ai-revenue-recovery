from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(50), unique=True)
    payment_id = Column(String(50), nullable=True)
    actor = Column(String(50), default="system")
    action = Column(String(255), nullable=False)
    input_summary = Column(Text)
    result = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())