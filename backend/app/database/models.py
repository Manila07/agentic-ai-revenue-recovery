# Import all models to ensure they are registered
from app.models.payment import Payment
from app.models.customer import Customer
from app.models.recovery import RecoveryAttempt
from app.models.agent_action import AgentAction
from app.models.audit_log import AuditLog