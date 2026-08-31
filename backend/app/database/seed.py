import sys
import os
from pathlib import Path

# Add project root and backend to sys.path
project_root = Path(__file__).resolve().parent.parent.parent  # up to project root
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

# Now import normally
from sqlalchemy.orm import Session
from app.database.models import Customer, Payment, RecoveryAttempt, AgentAction, AuditLog
from payments.simulator.payment_simulator import PaymentSimulator
import random

def seed_database(db: Session):
    # Clear existing data in correct order (respect foreign keys)
    db.query(AuditLog).delete()
    db.query(AgentAction).delete()
    db.query(RecoveryAttempt).delete()
    db.query(Payment).delete()
    db.query(Customer).delete()
    db.commit()

    simulator = PaymentSimulator()
    customers_data = [
        ("cust_001", "john@example.com", "John Doe", "premium"),
        ("cust_002", "jane@example.com", "Jane Smith", "standard"),
        ("cust_003", "bob@example.com", "Bob Wilson", "standard"),
        ("cust_004", "alice@example.com", "Alice Brown", "enterprise"),
    ]

    for cust_id, email, name, segment in customers_data:
        customer = Customer(
            id=cust_id,
            email=email,
            name=name,
            segment=segment,
            total_payments=random.randint(10, 50),
            successful_payments=random.randint(5, 40),
            failed_payments=random.randint(1, 10),
        )
        db.add(customer)

    # Generate sample failed payments
    for _ in range(20):
        customer_id = random.choice(["cust_001", "cust_002", "cust_003", "cust_004"])
        payment_data = simulator.generate_failed_transaction(
            customer_id=customer_id,
            amount=random.uniform(100, 5000),
        )
        payment = Payment(
            id=payment_data["id"],
            customer_id=payment_data["customer_id"],
            amount=payment_data["amount"],
            currency=payment_data["currency"],
            method=payment_data["method"],
            status=payment_data["status"],
            failure_reason=payment_data["failure_reason"],
            failure_category=payment_data["failure_category"],
        )
        db.add(payment)

    db.commit()
    print("Database seeded successfully.")