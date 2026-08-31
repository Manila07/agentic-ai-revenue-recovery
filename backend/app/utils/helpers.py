import hashlib
import uuid
from datetime import datetime

def generate_id(prefix: str = "") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def hash_string(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def format_currency(amount: float) -> str:
    return f"₹{amount:,.2f}"

def get_current_timestamp() -> str:
    return datetime.now().isoformat()