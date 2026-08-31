from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class AgentAction(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String(50), ForeignKey("payments.id"), nullable=False)
    decision = Column(String(50), nullable=False)
    reasoning = Column(Text)
    confidence = Column(Float, default=0.0)
    tool_name = Column(String(100))
    tool_args = Column(Text)
    status = Column(String(20), default="PROPOSED")
    created_at = Column(DateTime, server_default=func.now())