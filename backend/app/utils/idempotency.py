import hashlib
from app.database.models import AuditLog

def generate_idempotency_key(payment_id: str, action: str) -> str:
    key = f"{payment_id}:{action}"
    return hashlib.sha256(key.encode()).hexdigest()

def is_duplicate(db, payment_id: str, action: str) -> bool:
    key = generate_idempotency_key(payment_id, action)
    existing = db.query(AuditLog).filter(
        AuditLog.input_summary.like(f"%{key}%"),
        AuditLog.action == f"EXECUTE_{action}",
    ).first()
    return existing is not None